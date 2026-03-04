from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category,
    Product,
    ProductImage,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Review,
    UserProfile,
    Wishlist,
)


class AdminMultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class AdminMultipleFileField(forms.FileField):
    def clean(self, data, initial=None):
        if not data:
            return []
        if not isinstance(data, (list, tuple)):
            data = [data]
        cleaned_files = []
        for uploaded_file in data:
            cleaned_files.append(super().clean(uploaded_file, initial))
        return cleaned_files


class ProductAdminForm(forms.ModelForm):
    gallery_upload = AdminMultipleFileField(
        required=False,
        widget=AdminMultipleFileInput(attrs={'multiple': True}),
        help_text='Select one or more gallery images for this product.',
        label='Gallery Images',
    )

    class Meta:
        model = Product
        fields = '__all__'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 2
    fields = ('image', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit:cover;border-radius:8px;" />',
                obj.image.url,
            )
        return '-'

    preview.short_description = 'Preview'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    list_per_page = 25

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('products')

    def product_count(self, obj):
        return obj.products.count()

    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = (
        'name',
        'category',
        'price',
        'discount_price',
        'stock',
        'colored_status',
        'rating',
        'is_featured',
        'created_at',
    )
    list_filter = ('category', 'status', 'is_featured', 'created_at')
    search_fields = ('name', 'description')
    exclude = ('slug',)
    readonly_fields = ('created_at', 'updated_at', 'display_image')
    list_editable = ('is_featured', 'stock')
    date_hierarchy = 'created_at'
    list_select_related = ('category',)
    list_per_page = 25
    actions = ('mark_featured', 'mark_not_featured')
    inlines = [ProductImageInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'short_description', 'description')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'discount_price', 'stock', 'status')
        }),
        ('Media & Features', {
            'fields': ('image', 'display_image', 'gallery_upload', 'is_featured')
        }),
        ('Ratings & Timestamps', {
            'fields': ('rating', 'created_at', 'updated_at')
        }),
    )
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="140" height="140" style="object-fit:cover;border-radius:10px;" />', obj.image.url)
        return "No image"
    display_image.short_description = 'Product Image'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        gallery_files = request.FILES.getlist('gallery_upload')
        for image_file in gallery_files:
            ProductImage.objects.create(product=obj, image=image_file)

    def colored_status(self, obj):
        status_colors = {
            'in_stock': '#16a34a',
            'low_stock': '#f59e0b',
            'out_of_stock': '#dc2626',
        }
        color = status_colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="font-weight:600;color:{};">{}</span>',
            color,
            obj.get_status_display(),
        )

    colored_status.short_description = 'Status'
    colored_status.admin_order_field = 'status'

    @admin.action(description='Mark selected products as Featured')
    def mark_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} product(s) marked as featured.')

    @admin.action(description='Remove Featured flag from selected products')
    def mark_not_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} product(s) updated.')


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_count', 'cart_total', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at')
    list_select_related = ('user',)
    list_per_page = 25
    inlines = [CartItemInline]

    def item_count(self, obj):
        return obj.get_item_count()

    item_count.short_description = 'Items'

    def cart_total(self, obj):
        return obj.get_total()

    cart_total.short_description = 'Total'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'get_total')
    list_filter = ('created_at',)
    search_fields = ('product__name', 'cart__user__username')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('product', 'cart')
    list_select_related = ('product', 'cart', 'cart__user')
    list_per_page = 25
    
    def get_total(self, obj):
        return obj.get_total()
    get_total.short_description = 'Total Price'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'user',
        'colored_status',
        'payment_status',
        'total_price',
        'created_at',
    )
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('order_number', 'user__username', 'email')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    list_editable = ('payment_status',)
    date_hierarchy = 'created_at'
    list_select_related = ('user',)
    list_per_page = 25
    actions = ('mark_processing', 'mark_shipped', 'mark_delivered', 'mark_cancelled')
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'total_price', 'status', 'payment_method', 'payment_status')
        }),
        ('Shipping Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'postal_code')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def colored_status(self, obj):
        status_colors = {
            'pending': '#f59e0b',
            'processing': '#2563eb',
            'shipped': '#7c3aed',
            'delivered': '#16a34a',
            'cancelled': '#dc2626',
        }
        color = status_colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="font-weight:600;color:{};">{}</span>',
            color,
            obj.get_status_display(),
        )

    colored_status.short_description = 'Status'
    colored_status.admin_order_field = 'status'

    @admin.action(description='Mark selected orders as Processing')
    def mark_processing(self, request, queryset):
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} order(s) marked as processing.')

    @admin.action(description='Mark selected orders as Shipped')
    def mark_shipped(self, request, queryset):
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} order(s) marked as shipped.')

    @admin.action(description='Mark selected orders as Delivered')
    def mark_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f'{updated} order(s) marked as delivered.')

    @admin.action(description='Mark selected orders as Cancelled')
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} order(s) marked as cancelled.')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'get_total')
    list_filter = ('order__created_at',)
    search_fields = ('order__order_number', 'product__name')
    readonly_fields = ('order', 'product', 'quantity', 'price')
    autocomplete_fields = ('order', 'product')
    list_select_related = ('order', 'product')
    list_per_page = 25
    
    def get_total(self, obj):
        return obj.get_total()
    get_total.short_description = 'Total Price'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('product', 'user')
    list_select_related = ('product', 'user')
    list_per_page = 25


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'display_avatar')
    autocomplete_fields = ('user',)
    list_select_related = ('user',)
    list_per_page = 25
    
    def display_avatar(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="80" height="80" style="object-fit:cover;border-radius:999px;" />', obj.avatar.url)
        return "No avatar"
    display_avatar.short_description = 'Avatar'


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_count', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)
    autocomplete_fields = ('user', 'products')
    list_select_related = ('user',)
    list_per_page = 25
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products in Wishlist'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'preview', 'created_at')
    search_fields = ('product__name',)
    list_select_related = ('product',)
    list_per_page = 25

    def preview(self, obj):
        return format_html('<img src="{}" width="90" height="90" style="object-fit:cover;border-radius:8px;" />', obj.image.url)

    preview.short_description = 'Image Preview'
