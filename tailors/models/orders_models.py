from django.db import models
from django.contrib.auth.models import User
from .shop_models import Product, ProductVariation

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending Payment', 'Pending Payment'),
        ('Paid', 'Paid'),
        ('In Progress', 'In Progress (Stitching)'),
        ('Completed', 'Completed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending Payment')
    created_at = models.DateTimeField(auto_now_add=True)
    shipping_address = models.TextField(blank=True)
    stripe_checkout_id = models.CharField(max_length=255, blank=True, null=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(ProductVariation, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
