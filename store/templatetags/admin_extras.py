from decimal import Decimal

from django import template
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum

from store.models import Category, Order, Product

register = template.Library()


@register.simple_tag
def get_admin_stats():
    total_revenue = Order.objects.aggregate(total=Sum('total_price')).get('total') or Decimal('0')
    pending_orders = Order.objects.filter(status='pending').count()
    processing_orders = Order.objects.filter(status='processing').count()
    low_stock_products = Product.objects.filter(stock__gt=0, stock__lte=10).count()
    out_of_stock_products = Product.objects.filter(stock=0).count()
    recent_orders = (
        Order.objects.select_related('user')
        .order_by('-created_at')[:6]
    )
    low_stock_items = (
        Product.objects.filter(stock__gt=0, stock__lte=10)
        .select_related('category')
        .order_by('stock', 'name')[:6]
    )
    top_categories = (
        Category.objects.annotate(total_products=Count('products'))
        .order_by('-total_products', 'name')[:5]
    )
    return {
        'products': Product.objects.count(),
        'categories': Category.objects.count(),
        'orders': Order.objects.count(),
        'customers': get_user_model().objects.count(),
        'revenue': total_revenue,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'low_stock_products': low_stock_products,
        'out_of_stock_products': out_of_stock_products,
        'recent_orders': recent_orders,
        'low_stock_items': low_stock_items,
        'top_categories': top_categories,
    }
