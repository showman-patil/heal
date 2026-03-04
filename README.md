# 🌿 Heal-Delight E-Commerce Platform

A modern, professional e-commerce website for premium health and wellness products built with Django, HTML, TailwindCSS, and JavaScript.

## ✨ Features

### 🛍️ Shopping Experience
- **Dynamic Product Catalog**: Browse products with advanced filtering, sorting, and search
- **Product Details**: Detailed product pages with images, descriptions, pricing, and customer reviews
- **Shopping Cart**: Add/remove items, update quantities, and dynamic price calculations
- **Wishlist**: Save favorite products for later
- **Reviews & Ratings**: Customer reviews with star ratings
- **Stock Management**: Real-time inventory tracking

### 👤 User Management
- **User Registration & Authentication**: Secure account creation and login
- **User Profiles**: Complete profile management with avatars and personal information
- **Order History**: Track all past orders and their statuses
- **Secure Authentication**: Password reset functionality

### 🛒 E-Commerce Features
- **Shopping Cart System**: Full-featured shopping cart with persistent storage
- **Checkout Process**: Multi-step checkout with shipping and payment information
- **Order Management**: Complete order tracking system with status updates
- **Order Confirmation**: Detailed order confirmation pages and email notifications (can be added)
- **Payment Methods**: Support for multiple payment methods (COD, UPI, Net Banking, Card)

### 🎨 Design & UX
- **Responsive Design**: Mobile-first, works seamlessly on all devices
- **Modern UI**: Built with TailwindCSS for a professional look
- **Smooth Animations**: Hover effects and transitions for better UX
- **Optimized Images**: Lazy loading and responsive images
- **Accessibility**: Semantic HTML and ARIA labels

### 🔒 Admin Features
- **Django Admin Panel**: Comprehensive admin interface
- **Product Management**: Add, edit, delete products and categories
- **Order Management**: Track and manage customer orders
- **User Management**: Manage user accounts and profiles
- **Inventory Management**: Monitor and update stock levels
- **Analytics**: View order statistics and sales data

### 📱 Additional Features
- **Category Management**: Organize products by categories
- **Search & Filtering**: Advanced product search with multiple filters
- **Discount System**: Support for percentage-based discounts
- **Featured Products**: Highlight special products on homepage
- **Cart Persistence**: Cart data saved in database per user

## 🛠️ Tech Stack

- **Backend**: Django 4.2+
- **Frontend**: HTML5, TailwindCSS, JavaScript
- **Database**: SQLite (production: PostgreSQL recommended)
- **Image Handling**: Pillow
- **Middleware**: Django-CORS-Headers

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual Environment (recommended)

## 🚀 Installation & Setup

### 1. Clone/Download the Project

```bash
cd c:\Users\rahul\OneDrive\Desktop\heal\heal_delight
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account:
- Username: admin
- Email: admin@example.com
- Password: (enter your password)

### 6. Add Sample Data

```bash
python manage.py shell
```

```python
from store.models import Category, Product
from decimal import Decimal

# Create Categories
cat1 = Category.objects.create(name="Vitamins & Supplements", slug="vitamins-supplements")
cat2 = Category.objects.create(name="Organic Foods", slug="organic-foods")
cat3 = Category.objects.create(name="Health Drinks", slug="health-drinks")

# Create Sample Products
Product.objects.create(
    name="Vitamin D3 Supplement",
    slug="vitamin-d3",
    category=cat1,
    description="Premium Vitamin D3 supplement for bone health and immunity",
    short_description="Supports bone health and immunity",
    price=Decimal("499.00"),
    discount_price=Decimal("399.00"),
    image="https://via.placeholder.com/400x400?text=Vitamin+D3",
    stock=50,
    rating=4.5,
    is_featured=True,
    status="in_stock"
)

Product.objects.create(
    name="Organic Green Tea",
    slug="organic-green-tea",
    category=cat2,
    description="Premium organic green tea from the mountains",
    short_description="Pure organic green tea",
    price=Decimal("299.00"),
    image="https://via.placeholder.com/400x400?text=Green+Tea",
    stock=100,
    rating=4.8,
    is_featured=True,
    status="in_stock"
)

Product.objects.create(
    name="Protein Shake Mix",
    slug="protein-shake",
    category=cat3,
    description="High-protein shake mix for fitness enthusiasts",
    short_description="Complete protein formula",
    price=Decimal("799.00"),
    discount_price=Decimal("599.00"),
    image="https://via.placeholder.com/400x400?text=Protein+Shake",
    stock=75,
    rating=4.6,
    is_featured=True,
    status="in_stock"
)

print("Sample data created successfully!")
exit()
```

### 7. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 8. Run Development Server

```bash
python manage.py runserver
```

The website will be available at: **http://127.0.0.1:8000**

## 📍 Important URLs

| Page | URL |
|------|-----|
| Home | http://127.0.0.1:8000/ |
| Products | http://127.0.0.1:8000/products/ |
| Login | http://127.0.0.1:8000/login/ |
| Register | http://127.0.0.1:8000/register/ |
| Shopping Cart | http://127.0.0.1:8000/cart/ |
| Checkout | http://127.0.0.1:8000/checkout/ |
| My Profile | http://127.0.0.1:8000/account/profile/ |
| My Orders | http://127.0.0.1:8000/account/orders/ |
| Wishlist | http://127.0.0.1:8000/wishlist/ |
| Admin Panel | http://127.0.0.1:8000/admin/ |

## 🎯 User Guide

### For Customers

1. **Browse Products**: Visit the Products page to see all available items
2. **Search & Filter**: Use search bar and filters to find products
3. **View Details**: Click on a product to see full details and reviews
4. **Add to Cart**: Click "Add to Cart" to add items to your shopping cart
5. **Manage Cart**: Update quantities or remove items from your cart
6. **Checkout**: Proceed to checkout and enter shipping information
7. **Place Order**: Select payment method and complete your purchase
8. **Track Order**: View your order status in the Orders section

### For Administrators

1. **Login to Admin**: Go to `/admin/` with your superuser credentials
2. **Manage Products**: Add, edit, or delete products
3. **Manage Categories**: Create and manage product categories
4. **View Orders**: See all customer orders and update their status
5. **User Management**: Manage customer accounts and profiles
6. **View Reports**: Check sales statistics and order details

## 📊 Database Models

### Core Models
- **Product**: Product information with pricing and inventory
- **Category**: Product categories
- **Cart**: Shopping cart for each user
- **CartItem**: Individual items in a cart
- **Order**: Customer orders
- **OrderItem**: Items in an order
- **Review**: Product reviews with ratings
- **UserProfile**: Extended user information
- **Wishlist**: User's wishlist

## 🔐 Security Features

- ✅ CSRF Protection
- ✅ SQL Injection Prevention
- ✅ XSS Protection
- ✅ Secure Password Hashing
- ✅ User Authentication & Authorization
- ✅ CORS Headers Configuration

## 📦 Project Structure

```
heal_delight/
├── heal_delight/          # Main project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI configuration
├── store/                 # Main app
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── urls.py            # App URLs
│   ├── forms.py           # Django forms
│   ├── admin.py           # Admin configuration
│   └── signals.py         # Signal handlers
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── home.html          # Homepage
│   ├── products/          # Product pages
│   ├── auth/              # Authentication pages
│   ├── cart/              # Cart pages
│   ├── checkout/          # Checkout pages
│   └── account/           # User account pages
├── static/                # CSS, JS, Images
├── manage.py              # Django management
└── requirements.txt       # Python dependencies
```

## 🚀 Deployment

### For Production

1. **Environment Variables**: Create a `.env` file with:
   ```
   DEBUG=False
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=yourdomain.com
   DATABASE_URL=postgresql://...
   ```

2. **Use PostgreSQL**: Install and configure PostgreSQL
3. **Collect Static Files**: `python manage.py collectstatic`
4. **Use Gunicorn**: Install and configure Gunicorn
5. **Use Nginx**: Set up Nginx as reverse proxy
6. **Enable HTTPS**: Configure SSL/TLS certificates
7. **Set DEBUG=False**: Disable debug mode

### Deployment Platforms
- Heroku
- AWS
- DigitalOcean
- PythonAnywhere
- Render.com

## 🐛 Troubleshooting

### Issue: "Module not found"
**Solution**: Ensure virtual environment is activated and all dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: "No such table"
**Solution**: Run migrations
```bash
python manage.py migrate
```

### Issue: "Static files not loading"
**Solution**: Collect static files
```bash
python manage.py collectstatic --noinput
```

### Issue: "Permission denied" on uploads
**Solution**: Create media folder with proper permissions
```bash
mkdir media
chmod 755 media
```

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Django Models](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Django Forms](https://docs.djangoproject.com/en/stable/topics/forms/)

## 🤝 Contributing

To contribute to this project:
1. Create a new branch
2. Make your changes
3. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 💬 Support

For support and questions:
- Email: support@heal-delight.com
- Issues: Create an issue on GitHub

## 🎉 Features Coming Soon

- ✨ Email notifications for orders
- ✨ Payment gateway integration
- ✨ Advanced analytics dashboard
- ✨ Customer support chat
- ✨ Product recommendations
- ✨ Subscription plans
- ✨ Mobile app

---

**Made with ❤️ for health-conscious customers**

**Version**: 1.0.0  
**Last Updated**: March 2024
