import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MZtailors.settings')
django.setup()

from tailors.models import Category

def create_categories():
    categories_data = [
        {
            'name': "Men's Suits",
            'description': 'Bespoke suits tailored to perfection',
            'order': 1
        },
        {
            'name': "Women's Dresses",
            'description': 'Elegant designs for every occasion',
            'order': 2
        },
        {
            'name': 'Pants & Trousers',
            'description': 'Perfect fit for every style',
            'order': 3
        },
        {
            'name': 'Waistcoats',
            'description': 'Classic vests for formal occasions',
            'order': 4
        },
        {
            'name': 'Wedding Attire',
            'description': 'Make your special day perfect',
            'order': 5
        },
        {
            'name': 'Coats & Jackets',
            'description': 'Outerwear for all seasons',
            'order': 6
        },
        {
            'name': 'Alterations',
            'description': 'Expert fitting and adjustments',
            'order': 7
        },
        {
            'name': 'Formal Shirts',
            'description': 'Custom shirts for business & events',
            'order': 8
        }
    ]
    
    for category_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=category_data['name'],
            defaults=category_data
        )
        if created:
            print(f"Created category: {category.name}")
    
    print("Categories created successfully!")

if __name__ == '__main__':
    create_categories()