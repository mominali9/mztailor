from django.db import models
from django.contrib.auth.models import User
from .base_models import Category

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    size = models.CharField(max_length=50, choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'), ('Custom', 'Customized')])
    color = models.CharField(max_length=50)
    stock_quantity = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.product.name} - {self.size} / {self.color}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(ProductVariation, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.product.price
