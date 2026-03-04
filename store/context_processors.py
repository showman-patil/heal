from datetime import datetime

from .models import Cart, Wishlist


def global_context(request):
    cart_count = 0
    wishlist_count = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        wishlist = Wishlist.objects.filter(user=request.user).first()
        cart_count = cart.get_item_count() if cart else 0
        wishlist_count = wishlist.products.count() if wishlist else 0

    return {
        'current_year': datetime.now().year,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
    }
