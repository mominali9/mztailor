import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MZtailors.settings')
django.setup()

from django.contrib.auth.models import User
from tailors.models import Article, Service, Testimonial

def create_sample_data():
    # Create superuser if not exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@mztailors.com', 'admin123')
        print("Admin user created")
    
    admin_user = User.objects.get(username='admin')
    
    # Create Services
    services_data = [
        {
            'name': 'Custom Suit Tailoring',
            'description': 'Bespoke suits crafted to your exact measurements with premium fabrics and attention to detail.',
            'price': 899.00
        },
        {
            'name': 'Wedding Dress Design',
            'description': 'Custom wedding dresses designed to make your special day unforgettable.',
            'price': 1299.00
        },
        {
            'name': 'Shirt Alterations',
            'description': 'Professional shirt fitting and alterations for the perfect fit.',
            'price': 45.00
        },
        {
            'name': 'Formal Wear Rental',
            'description': 'High-quality formal wear rental for special occasions and events.',
            'price': 150.00
        },
        {
            'name': 'Trouser Hemming',
            'description': 'Expert trouser hemming and adjustments for the perfect length.',
            'price': 25.00
        },
        {
            'name': 'Dress Alterations',
            'description': 'Professional dress alterations and fitting services.',
            'price': 65.00
        }
    ]
    
    for service_data in services_data:
        service, created = Service.objects.get_or_create(
            name=service_data['name'],
            defaults=service_data
        )
        if created:
            print(f"Created service: {service.name}")
    
    # Create Articles
    articles_data = [
        {
            'title': 'The Art of Bespoke Tailoring',
            'content': 'Bespoke tailoring is more than just creating clothes; it\'s an art form that has been perfected over centuries. At MZ Tailors, we continue this tradition by combining time-honored techniques with modern innovations. Our master tailors spend years learning the craft, understanding how different fabrics behave, and mastering the subtle art of creating garments that not only fit perfectly but also reflect the wearer\'s personality and style. From the initial consultation to the final fitting, every step is carefully orchestrated to ensure that each piece is truly unique.',
            'author': admin_user,
            'is_published': True
        },
        {
            'title': 'Choosing the Right Fabric for Your Suit',
            'content': 'The fabric you choose for your suit can make all the difference in how it looks, feels, and performs. Wool remains the most popular choice for its versatility and durability, but within wool, there are numerous options from lightweight tropical wools perfect for summer to heavy tweeds ideal for winter. Cotton and linen offer breathability for warmer climates, while silk adds luxury and sheen. At MZ Tailors, we source our fabrics from the finest mills around the world, ensuring that every suit we create uses only the highest quality materials.',
            'author': admin_user,
            'is_published': True
        },
        {
            'title': 'Wedding Dress Trends for 2024',
            'content': 'This year\'s wedding dress trends are all about personal expression and timeless elegance. We\'re seeing a return to classic silhouettes with modern twists - think A-line dresses with unexpected details, minimalist designs with luxurious fabrics, and vintage-inspired gowns with contemporary updates. Sustainability is also playing a bigger role, with many brides choosing eco-friendly fabrics and designs that can be worn again. At MZ Tailors, we work closely with each bride to create a dress that reflects her unique style while incorporating the latest trends.',
            'author': admin_user,
            'is_published': True
        }
    ]
    
    for article_data in articles_data:
        article, created = Article.objects.get_or_create(
            title=article_data['title'],
            defaults=article_data
        )
        if created:
            print(f"Created article: {article.title}")
    
    # Create Testimonials
    testimonials_data = [
        {
            'customer_name': 'James Wilson',
            'message': 'Absolutely exceptional service! My wedding suit was perfect in every detail. The team at MZ Tailors truly understands craftsmanship.',
            'rating': 5,
            'is_approved': True
        },
        {
            'customer_name': 'Sarah Johnson',
            'message': 'I had my wedding dress made here and it exceeded all my expectations. The attention to detail and quality is unmatched.',
            'rating': 5,
            'is_approved': True
        },
        {
            'customer_name': 'Michael Brown',
            'message': 'Professional alterations service with quick turnaround. My suits fit perfectly now. Highly recommended!',
            'rating': 5,
            'is_approved': True
        },
        {
            'customer_name': 'Emily Davis',
            'message': 'The custom dress I ordered was exactly what I envisioned. Great communication throughout the process.',
            'rating': 4,
            'is_approved': True
        },
        {
            'customer_name': 'Robert Miller',
            'message': 'Outstanding quality and service. Been coming here for years and never disappointed.',
            'rating': 5,
            'is_approved': True
        }
    ]
    
    for testimonial_data in testimonials_data:
        testimonial, created = Testimonial.objects.get_or_create(
            customer_name=testimonial_data['customer_name'],
            defaults=testimonial_data
        )
        if created:
            print(f"Created testimonial: {testimonial.customer_name}")
    
    print("Sample data creation completed!")

if __name__ == '__main__':
    create_sample_data()