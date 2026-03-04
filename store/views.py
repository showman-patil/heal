from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
import uuid

from .models import Product, Category, Cart, CartItem, Order, OrderItem, Review, UserProfile, Wishlist
from .forms import (
    UserRegistrationForm, UserLoginForm, UserProfileForm, 
    ReviewForm, CheckoutForm
)


def home(request):
    """Home page with featured products"""
    featured_products = Product.objects.filter(is_featured=True)[:8]
    categories = Category.objects.annotate(product_count=Count('products')).order_by('name')[:6]

    stats = {
        'products': Product.objects.count(),
        'categories': Category.objects.count(),
        'customers': User.objects.count(),
    }

    context = {
        'featured_products': featured_products,
        'categories': categories,
        'stats': stats,
    }
    return render(request, 'home.html', context)


def product_list(request):
    """Product listing with filters and search"""
    products = Product.objects.all()
    categories = Category.objects.all()
    query_params = request.GET.copy()
    query_params.pop('sort', None)
    query_params.pop('page', None)
    
    # Search
    query = request.GET.get('q', '')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(short_description__icontains=query)
        )
    
    # Category filter
    category = request.GET.get('category', '')
    if category:
        products = products.filter(category__slug=category)
    
    # Sorting
    sort = request.GET.get('sort', '-created_at')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-rating')
    else:
        products = products.order_by(sort)
    
    # Pagination
    paginator = Paginator(products, 12)
    page = request.GET.get('page', 1)
    products = paginator.get_page(page)
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category,
        'query': query,
        'sort': sort,
        'base_query': query_params.urlencode(),
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug)
    gallery_images = product.gallery_images.all()
    product_images = []
    if product.image:
        product_images.append({'url': product.image.url, 'alt': product.name})
    for gallery_image in gallery_images:
        product_images.append({'url': gallery_image.image.url, 'alt': f'{product.name} image'})

    reviews = product.reviews.all()
    review_data = reviews.aggregate(avg_rating=Avg('rating'))
    average_rating = review_data['avg_rating'] or 0
    review_count = reviews.count()
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    can_review = False
    user_review = None
    
    if request.user.is_authenticated:
        user_review = product.reviews.filter(user=request.user).first()
        can_review = request.user.orders.filter(items__product=product).exists()
    
    if request.method == 'POST' and can_review:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review, created = Review.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={
                    'rating': form.cleaned_data['rating'],
                    'comment': form.cleaned_data['comment'],
                }
            )
            product.rating = product.reviews.aggregate(avg_rating=Avg('rating')).get('avg_rating') or 0
            product.save(update_fields=['rating'])
            messages.success(request, 'Review submitted successfully!')
            return redirect('product_detail', slug=slug)
    else:
        form = ReviewForm()
    
    context = {
        'product': product,
        'gallery_images': gallery_images,
        'product_images': product_images,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_count': review_count,
        'related_products': related_products,
        'can_review': can_review,
        'form': form,
        'user_review': user_review,
    }
    return render(request, 'products/product_detail.html', context)


# Authentication Views
def register(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')


# Cart Views
@login_required(login_url='login')
def cart_view(request):
    """View shopping cart"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    context = {
        'cart': cart,
        'total': cart.get_total(),
        'item_count': cart.get_item_count(),
    }
    return render(request, 'cart/cart.html', context)


@login_required(login_url='login')
def add_to_cart(request, slug):
    """Add product to cart"""
    product = get_object_or_404(Product, slug=slug)
    cart, created = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if product.stock < quantity:
        messages.error(request, 'Insufficient stock!')
        return redirect('product_detail', slug=slug)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        if cart_item.quantity > product.stock:
            messages.error(request, 'Insufficient stock!')
            return redirect('cart')
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart')


@login_required(login_url='login')
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('cart')


@login_required(login_url='login')
def update_cart(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0:
        cart_item.delete()
        messages.success(request, 'Item removed from cart!')
    elif quantity > cart_item.product.stock:
        messages.error(request, 'Insufficient stock!')
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated!')
    
    return redirect('cart')


# Checkout Views
@login_required(login_url='login')
def checkout(request):
    """Checkout page"""
    cart = get_object_or_404(Cart, user=request.user)
    
    if cart.items.count() == 0:
        messages.error(request, 'Your cart is empty!')
        return redirect('products')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order
            order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
            order = Order.objects.create(
                user=request.user,
                order_number=order_number,
                total_price=cart.get_total(),
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                postal_code=form.cleaned_data['postal_code'],
                payment_method=form.cleaned_data['payment_method'],
            )
            
            # Create order items
            for cart_item in cart.items.all():
                price = cart_item.product.discount_price or cart_item.product.price
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=price,
                )
                
                # Update stock
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()
            
            # Clear cart
            cart.items.all().delete()
            
            messages.success(request, f'Order placed successfully! Order #: {order_number}')
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm(initial={
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        })
    
    context = {
        'form': form,
        'cart': cart,
        'total': cart.get_total(),
    }
    return render(request, 'checkout/checkout.html', context)


@login_required(login_url='login')
def order_confirmation(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
        'items': order.items.all(),
    }
    return render(request, 'checkout/order_confirmation.html', context)


# User Profile Views
@login_required(login_url='login')
def profile(request):
    """User profile page"""
    profile = get_object_or_404(UserProfile, user=request.user)
    orders = request.user.orders.all()
    
    context = {
        'profile': profile,
        'orders': orders,
    }
    return render(request, 'account/profile.html', context)


@login_required(login_url='login')
def edit_profile(request):
    """Edit user profile"""
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {'form': form}
    return render(request, 'account/edit_profile.html', context)


@login_required(login_url='login')
def order_list(request):
    """User's order history"""
    orders = request.user.orders.all()
    paginator = Paginator(orders, 10)
    page = request.GET.get('page', 1)
    orders = paginator.get_page(page)
    
    context = {'orders': orders}
    return render(request, 'account/order_list.html', context)


@login_required(login_url='login')
def order_detail(request, order_id):
    """Order details page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()
    
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'account/order_detail.html', context)


# Wishlist Views
@login_required(login_url='login')
def wishlist(request):
    """View wishlist"""
    wishlist = get_object_or_404(Wishlist, user=request.user)
    products = wishlist.products.all()
    
    context = {'products': products}
    return render(request, 'wishlist.html', context)


@login_required(login_url='login')
def add_to_wishlist(request, slug):
    """Add product to wishlist"""
    product = get_object_or_404(Product, slug=slug)
    wishlist = get_object_or_404(Wishlist, user=request.user)
    
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        messages.info(request, f'{product.name} removed from wishlist!')
    else:
        wishlist.products.add(product)
        messages.success(request, f'{product.name} added to wishlist!')
    
    return redirect('product_detail', slug=slug)
