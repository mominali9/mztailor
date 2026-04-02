from django.db import models
from django.contrib.auth.models import User

class Logo(models.Model):
    name = models.CharField(max_length=100, default='MZ Tailors')
    logo_image = models.ImageField(upload_to='logos/')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='categories/')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    video_url = models.URLField(blank=True, help_text='YouTube or Vimeo URL')
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    background_image = models.ImageField(upload_to='hero_backgrounds/', blank=True, null=True, help_text='Background image for hero section')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-id']
    
    def __str__(self):
        return self.title

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    message = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customer_name} - {self.rating} stars"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.email}"

class Statistics(models.Model):
    happy_customers = models.IntegerField(default=2500, help_text='Number of happy customers')
    years_experience = models.IntegerField(default=25, help_text='Years of experience')
    expert_tailors = models.IntegerField(default=50, help_text='Number of expert tailors')
    satisfaction_rate = models.IntegerField(default=99, help_text='Satisfaction rate percentage')
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Statistics'
    
    def __str__(self):
        return f"Stats - {self.happy_customers} customers, {self.years_experience} years"
