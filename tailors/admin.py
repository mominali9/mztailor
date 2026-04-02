from django.contrib import admin

from .models import *

@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    list_editable = ['is_active']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at', 'author']
    search_fields = ['title', 'content']
    list_editable = ['is_published']
    prepopulated_fields = {}

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['price', 'is_active']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['customer_name', 'message']
    list_editable = ['is_approved']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'background_image', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'order']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'order']

@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ['id', 'happy_customers', 'years_experience', 'expert_tailors', 'satisfaction_rate', 'is_active', 'updated_at']
    list_filter = ['is_active', 'updated_at']
    list_editable = ['happy_customers', 'years_experience', 'expert_tailors', 'satisfaction_rate', 'is_active']
    list_display_links = ['id']

class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_active', 'created_at']
    list_filter = ['is_active', 'category']
    search_fields = ['name', 'description']
    inlines = [ProductVariationInline]

@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'color', 'stock_quantity']
    list_filter = ['size', 'color']

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'created_at']
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'shipping_address']
    list_editable = ['status']
    inlines = [OrderItemInline]

@admin.register(MeasurementProfile)
class MeasurementProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'height_cm', 'chest_cm', 'recommended_size', 'created_at']
    search_fields = ['user__username']    