import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MZtailors.settings')
django.setup()

from tailors.models import Service

def add_services():
    # Clear existing services to avoid duplicates
    Service.objects.all().delete()
    
    services_data = [
        {
            'name': 'Custom Suit Tailoring',
            'description': 'Bespoke suits crafted to your exact measurements with premium fabrics. Our master tailors ensure perfect fit and exceptional quality for business and formal occasions.',
            'price': 899.00
        },
        {
            'name': 'Wedding Dress Design',
            'description': 'Custom wedding dresses designed to make your special day unforgettable. From classic elegance to modern styles, we create the dress of your dreams.',
            'price': 1299.00
        },
        {
            'name': 'Formal Shirt Tailoring',
            'description': 'Custom-made formal shirts with precise measurements and premium cotton fabrics. Perfect for business meetings and special events.',
            'price': 125.00
        },
        {
            'name': 'Trouser Alterations',
            'description': 'Professional trouser hemming, waist adjustments, and tapering services. Expert alterations for the perfect fit.',
            'price': 35.00
        },
        {
            'name': 'Waistcoat Creation',
            'description': 'Elegant waistcoats and vests tailored to complement your suits. Available in various fabrics and styles.',
            'price': 245.00
        },
        {
            'name': 'Coat & Jacket Tailoring',
            'description': 'Custom coats and jackets for all seasons. From business blazers to winter overcoats, crafted with precision.',
            'price': 675.00
        },
        {
            'name': 'Dress Alterations',
            'description': 'Expert dress fitting and alterations for all occasions. Ensuring perfect fit and comfort for every body type.',
            'price': 65.00
        },
        {
            'name': 'Formal Wear Rental',
            'description': 'High-quality formal wear rental service for special occasions. Tuxedos, evening gowns, and accessories available.',
            'price': 150.00
        }
    ]
    
    for service_data in services_data:
        service = Service.objects.create(**service_data)
        print(f"Created service: {service.name} - ${service.price}")
    
    print("Services updated successfully!")

if __name__ == '__main__':
    add_services()