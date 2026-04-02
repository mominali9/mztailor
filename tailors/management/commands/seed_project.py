import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from tailors.models.base_models import Category, Service, Logo, Video, Statistics
from tailors.models.shop_models import Product, ProductVariation
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = 'Seeds the project with initial realistic data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # 1. Groups
        employee_group, _ = Group.objects.get_or_create(name='Employee')

        # 2. Users
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@mztailors.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created admin user: admin / admin123'))

        if not User.objects.filter(username='employee').exists():
            emp = User.objects.create_user('employee', 'employee@mztailors.com', 'emp123', is_staff=True)
            emp.groups.add(employee_group)
            self.stdout.write(self.style.SUCCESS('Created employee user: employee / emp123'))

        if not User.objects.filter(username='customer').exists():
            User.objects.create_user('customer', 'customer@gmail.com', 'cust123')
            self.stdout.write(self.style.SUCCESS('Created customer user: customer / cust123'))

        # 3. Categories
        categories_data = [
            {'name': 'Executive Suits', 'description': 'Premium bespoke suits for professionals', 'order': 1},
            {'name': 'Royal Waistcoats', 'description': 'Traditional and modern waistcoats', 'order': 2},
            {'name': 'Formal Shirts', 'description': 'Crisp, tailored shirts for every occasion', 'order': 3},
            {'name': 'Traditional Wear', 'description': 'Exquisite Sherwanis and Kurta Pajamas', 'order': 4},
        ]
        
        for cat_data in categories_data:
            Category.objects.get_or_create(name=cat_data['name'], defaults={
                'description': cat_data['description'],
                'order': cat_data['order']
            })
        self.stdout.write('Seeded Categories')

        # 4. Products
        suits_cat = Category.objects.get(name='Executive Suits')
        products_data = [
            {'name': 'Italian Wool 3-Piece', 'price': 450.00, 'desc': 'Super 120s Italian wool, bespoke fit.'},
            {'name': 'Navy Midnight Tuxedo', 'price': 550.00, 'desc': 'Satin lapels, perfect for black-tie events.'},
            {'name': 'Charcoal Business Suit', 'price': 395.00, 'desc': 'Durable and sharp for daily executive wear.'},
        ]
        
        for p_data in products_data:
            Product.objects.get_or_create(name=p_data['name'], defaults={
                'category': suits_cat,
                'price': p_data['price'],
                'description': p_data['desc']
            })
        self.stdout.write('Seeded Products')

        # 5. Services
        services_data = [
            {'name': 'Bespoke Stitching', 'price': 120.00, 'desc': 'Full custom measurements and multiple fittings.'},
            {'name': 'Express 24h Delivery', 'price': 30.00, 'desc': 'Urgent stitching for your emergency events.'},
            {'name': 'Suit Alterations', 'price': 45.00, 'desc': 'Resizing and repairing your existing wardrobe.'},
        ]
        for s_data in services_data:
            Service.objects.get_or_create(name=s_data['name'], defaults={
                'price': s_data['price'],
                'description': s_data['desc']
            })
        self.stdout.write('Seeded Services')

        # 6. Logo & Stats
        Logo.objects.get_or_create(id=1, defaults={'name': 'MZ Tailors Main', 'is_active': True})
        Statistics.objects.get_or_create(id=1, defaults={
            'happy_customers': 2500,
            'years_experience': 25,
            'expert_tailors': 45,
            'satisfaction_rate': 99
        })
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded all data!'))
