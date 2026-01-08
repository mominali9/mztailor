import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MZtailors.settings')
django.setup()

from tailors.models import Testimonial

def update_testimonials():
    # Clear existing testimonials
    Testimonial.objects.all().delete()
    
    # Create new testimonials with Pakistani names
    testimonials_data = [
        {
            'customer_name': 'Ahmed Hassan',
            'message': 'Outstanding work! My wedding sherwani was absolutely perfect. The craftsmanship and attention to detail exceeded my expectations.',
            'rating': 5,
            'is_approved': True
        },
        {
            'customer_name': 'Fatima Khan',
            'message': 'Excellent service for my daughter\'s wedding dress. The team understood our requirements perfectly and delivered a beautiful outfit.',
            'rating': 5,
            'is_approved': True
        },
        {
            'customer_name': 'Muhammad Ali',
            'message': 'Professional tailoring services with quick delivery. My business suits fit perfectly and the quality is exceptional.',
            'rating': 5,
            'is_approved': True
        },
        {
            'customer_name': 'Ayesha Malik',
            'message': 'Amazing experience! The custom dress alterations were done perfectly. Highly recommend MZ Tailors for quality work.',
            'rating': 4,
            'is_approved': True
        },
        {
            'customer_name': 'Usman Sheikh',
            'message': 'Been coming here for years. Consistent quality and excellent customer service. Best tailors in the city!',
            'rating': 5,
            'is_approved': True
        }
    ]
    
    for testimonial_data in testimonials_data:
        testimonial = Testimonial.objects.create(**testimonial_data)
        print(f"Created testimonial: {testimonial.customer_name} - {testimonial.rating} stars")
    
    print("Testimonials updated with Pakistani names!")

if __name__ == '__main__':
    update_testimonials()