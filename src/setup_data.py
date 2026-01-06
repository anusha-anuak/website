import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoestore.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from store.models import Category, Product
from django.core.files.base import ContentFile
import shutil

def create_data():
    # Create Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        print("Superuser 'admin' created.")

    # Update Site
    site = Site.objects.get_current()
    site.domain = '127.0.0.1:8000'
    site.name = 'ShoeStore'
    site.save()
    print("Site updated.")

    # Create Categories
    cat_sneakers, _ = Category.objects.get_or_create(name='Sneakers', slug='sneakers')
    cat_formal, _ = Category.objects.get_or_create(name='Formal', slug='formal')
    cat_boots, _ = Category.objects.get_or_create(name='Boots', slug='boots')

    # Create Products
    products_data = [
        {
            'category': cat_sneakers,
            'name': 'Air Fly 9000',
            'slug': 'air-fly-9000',
            'price': 129.99,
            'description': 'The ultimate running shoe with air cushion technology.',
            'stock': 50
        },
        {
            'category': cat_sneakers,
            'name': 'Street Walker Low',
            'slug': 'street-walker-low',
            'price': 89.50,
            'description': 'Classic style for everyday comfort.',
            'stock': 30
        },
        {
            'category': cat_formal,
            'name': 'Oxford Classic',
            'slug': 'oxford-classic',
            'price': 150.00,
            'description': 'Genuine leather oxfords for formal occasions.',
            'stock': 20
        },
        {
            'category': cat_boots,
            'name': 'Hiker Elite',
            'slug': 'hiker-elite',
            'price': 199.99,
            'description': 'Waterproof boots for the toughest terrains.',
            'stock': 15
        }
    ]

    for p_data in products_data:
        prod, created = Product.objects.get_or_create(
            slug=p_data['slug'],
            defaults={
                'category': p_data['category'],
                'name': p_data['name'],
                'price': p_data['price'],
                'description': p_data['description'],
                'stock': p_data['stock']
            }
        )
        if created:
            print(f"Product '{prod.name}' created.")

if __name__ == '__main__':
    create_data()
