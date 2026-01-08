import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MZtailors.settings')
django.setup()

from tailors.models import Service

def update_prices():
    # Update services with PKR prices
    services_updates = {
        'Custom Suit Tailoring': 25000,
        'Wedding Dress Design': 35000,
        'Formal Shirt Tailoring': 3500,
        'Trouser Alterations': 1200,
        'Waistcoat Creation': 8000,
        'Coat & Jacket Tailoring': 18000,
        'Dress Alterations': 2500,
        'Formal Wear Rental': 5000
    }
    
    for service_name, new_price in services_updates.items():
        try:
            service = Service.objects.get(name=service_name)
            service.price = new_price
            service.save()
            print(f"Updated {service_name}: PKR {new_price}")
        except Service.DoesNotExist:
            print(f"Service not found: {service_name}")
    
    print("All prices updated to PKR!")

if __name__ == '__main__':
    update_prices()