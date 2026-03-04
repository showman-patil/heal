import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heal_delight.settings')
django.setup()

from store.models import Category, Product
from decimal import Decimal

# Clear existing data
Product.objects.all().delete()
Category.objects.all().delete()

# Create categories
categories = [
    Category.objects.create(
        name='Vitamins & Supplements',
        slug='vitamins-supplements',
        description='Essential vitamins and dietary supplements for optimal health'
    ),
    Category.objects.create(
        name='Organic Products',
        slug='organic-products',
        description='100% organic and natural health products'
    ),
    Category.objects.create(
        name='Herbal Remedies',
        slug='herbal-remedies',
        description='Traditional herbal remedies and extracts'
    ),
    Category.objects.create(
        name='Skincare',
        slug='skincare',
        description='Natural skincare and beauty products'
    ),
    Category.objects.create(
        name='Fitness & Wellness',
        slug='fitness-wellness',
        description='Products for fitness and overall wellness'
    ),
    Category.objects.create(
        name='Superfoods',
        slug='superfoods',
        description='Nutrient-rich superfoods and powders'
    ),
]

# Create products
products_data = [
    {
        'name': 'Vitamin C Boost',
        'slug': 'vitamin-c-boost',
        'category': categories[0],
        'description': 'High-potency Vitamin C supplement to boost immunity and fight free radicals.',
        'short_description': 'Premium Vitamin C for immunity',
        'price': Decimal('12.99'),
        'discount_price': Decimal('9.99'),
        'stock': 50,
        'status': 'in_stock',
        'rating': Decimal('4.5'),
        'is_featured': True,
    },
    {
        'name': 'Organic Turmeric Powder',
        'slug': 'organic-turmeric-powder',
        'category': categories[1],
        'description': 'Pure organic turmeric powder with curcumin for anti-inflammatory benefits.',
        'short_description': 'Premium organic turmeric',
        'price': Decimal('14.99'),
        'discount_price': Decimal('11.99'),
        'stock': 45,
        'status': 'in_stock',
        'rating': Decimal('4.8'),
        'is_featured': True,
    },
    {
        'name': 'Ashwagandha Root Extract',
        'slug': 'ashwagandha-root-extract',
        'category': categories[2],
        'description': 'Concentrated ashwagandha extract to reduce stress and improve sleep quality.',
        'short_description': 'Natural stress relief',
        'price': Decimal('18.99'),
        'discount_price': Decimal('14.99'),
        'stock': 30,
        'status': 'in_stock',
        'rating': Decimal('4.6'),
        'is_featured': True,
    },
    {
        'name': 'Aloe Vera Gel',
        'slug': 'aloe-vera-gel',
        'category': categories[3],
        'description': 'Pure aloe vera gel for natural skin moisturization and healing.',
        'short_description': 'Natural skin moisturizer',
        'price': Decimal('9.99'),
        'discount_price': Decimal('7.99'),
        'stock': 60,
        'status': 'in_stock',
        'rating': Decimal('4.7'),
        'is_featured': False,
    },
    {
        'name': 'Protein Powder',
        'slug': 'protein-powder',
        'category': categories[4],
        'description': 'Plant-based protein powder for muscle building and recovery.',
        'short_description': 'Complete plant-based protein',
        'price': Decimal('24.99'),
        'discount_price': Decimal('19.99'),
        'stock': 40,
        'status': 'in_stock',
        'rating': Decimal('4.4'),
        'is_featured': True,
    },
    {
        'name': 'Spirulina Powder',
        'slug': 'spirulina-powder',
        'category': categories[5],
        'description': 'Nutrient-dense spirulina powder packed with proteins and minerals.',
        'short_description': 'Superfood spirulina',
        'price': Decimal('19.99'),
        'discount_price': Decimal('15.99'),
        'stock': 35,
        'status': 'in_stock',
        'rating': Decimal('4.5'),
        'is_featured': True,
    },
    {
        'name': 'Moringa Leaf Powder',
        'slug': 'moringa-leaf-powder',
        'category': categories[5],
        'description': 'Organic moringa leaf powder with 90+ nutrients and vitamins.',
        'short_description': 'Nutrient-rich moringa',
        'price': Decimal('16.99'),
        'discount_price': Decimal('13.99'),
        'stock': 50,
        'status': 'in_stock',
        'rating': Decimal('4.6'),
        'is_featured': False,
    },
    {
        'name': 'Ginger Root Capsules',
        'slug': 'ginger-root-capsules',
        'category': categories[2],
        'description': 'Premium ginger root capsules for digestion and circulation.',
        'short_description': 'Digestive support',
        'price': Decimal('11.99'),
        'discount_price': Decimal('9.49'),
        'stock': 55,
        'status': 'in_stock',
        'rating': Decimal('4.3'),
        'is_featured': False,
    },
    {
        'name': 'Charcoal Face Mask',
        'slug': 'charcoal-face-mask',
        'category': categories[3],
        'description': 'Deep cleansing activated charcoal mask for clear skin.',
        'short_description': 'Detoxifying face mask',
        'price': Decimal('13.99'),
        'discount_price': Decimal('10.99'),
        'stock': 70,
        'status': 'in_stock',
        'rating': Decimal('4.7'),
        'is_featured': False,
    },
    {
        'name': 'Omega-3 Fish Oil',
        'slug': 'omega-3-fish-oil',
        'category': categories[0],
        'description': 'Premium omega-3 fish oil for heart and brain health.',
        'short_description': 'Heart health supplement',
        'price': Decimal('22.99'),
        'discount_price': Decimal('18.99'),
        'stock': 25,
        'status': 'in_stock',
        'rating': Decimal('4.5'),
        'is_featured': True,
    },
    {
        'name': 'Probiotics Complex',
        'slug': 'probiotics-complex',
        'category': categories[0],
        'description': 'Multi-strain probiotic blend for gut health and immunity.',
        'short_description': 'Gut health support',
        'price': Decimal('19.99'),
        'discount_price': Decimal('15.99'),
        'stock': 40,
        'status': 'in_stock',
        'rating': Decimal('4.6'),
        'is_featured': False,
    },
    {
        'name': 'Honey & Cinnamon Blend',
        'slug': 'honey-cinnamon-blend',
        'category': categories[1],
        'description': 'Raw organic honey blended with cinnamon for natural energy.',
        'short_description': 'Natural energy boost',
        'price': Decimal('12.99'),
        'discount_price': Decimal('10.49'),
        'stock': 80,
        'status': 'in_stock',
        'rating': Decimal('4.8'),
        'is_featured': False,
    },
]

# Create products
for product_data in products_data:
    Product.objects.create(**product_data)

print("✓ Sample data added successfully!")
print(f"✓ Created {len(categories)} categories")
print(f"✓ Created {len(products_data)} products")
