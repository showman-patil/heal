from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Products
    path('products/', views.product_list, name='products'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='auth/password_reset.html',
            email_template_name='auth/password_reset_email.txt',
            subject_template_name='auth/password_reset_subject.txt',
        ),
        name='password_reset',
    ),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
    
    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    
    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    
    # Account
    path('account/profile/', views.profile, name='profile'),
    path('account/edit-profile/', views.edit_profile, name='edit_profile'),
    path('account/orders/', views.order_list, name='order_list'),
    path('account/order/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # Wishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<slug:slug>/', views.add_to_wishlist, name='add_to_wishlist'),
]
