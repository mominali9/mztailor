from django.urls import path
from tailors.views import public, shop, checkout, ai, api, auth, dashboards

urlpatterns = [
    # Public Pages
    path('', public.home, name='home'),
    path('articles/', public.articles_list, name='articles'),
    path('article/<int:pk>/', public.article_detail, name='article_detail'),
    path('services/', public.services, name='services'),
    path('about/', public.about, name='about'),
    path('contact/', public.contact, name='contact'),
    path('feedback/', public.feedback, name='feedback'),
    
    # Store & Cart
    path('shop/', shop.shop, name='shop'),
    path('product/<int:pk>/', shop.product_detail, name='product_detail'),
    path('cart/', shop.cart_view, name='cart'),
    path('checkout/', checkout.checkout_view, name='checkout'),
    path('customizer/', shop.customizer_view, name='customizer'),
    path('payment/success/', checkout.payment_success, name='payment_success'),
    
    # Authentication
    path('login/', auth.login_view, name='login'),
    path('register/', auth.register_view, name='register'),
    path('logout/', auth.logout_view, name='logout'),
    
    # Dashboards
    path('dashboard/', dashboards.dashboard_redirect, name='dashboard_redirect'),
    path('dashboard/admin/', dashboards.admin_dashboard, name='admin_dashboard'),
    path('dashboard/employee/', dashboards.employee_dashboard, name='employee_dashboard'),
    path('dashboard/customer/', dashboards.customer_dashboard, name='customer_dashboard'),

    # Custom Admin Management
    path('dashboard/admin/products/', dashboards.manage_products, name='manage_products'),
    path('dashboard/admin/products/add/', dashboards.product_upsert, name='product_create'),
    path('dashboard/admin/products/edit/<int:pk>/', dashboards.product_upsert, name='product_edit'),
    path('dashboard/admin/products/delete/<int:pk>/', dashboards.product_delete, name='product_delete'),
    
    path('dashboard/admin/categories/', dashboards.manage_categories, name='manage_categories'),
    path('dashboard/admin/categories/add/', dashboards.category_upsert, name='category_create'),
    path('dashboard/admin/categories/edit/<int:pk>/', dashboards.category_upsert, name='category_edit'),
    
    path('dashboard/admin/services/', dashboards.manage_services, name='manage_services'),
    path('dashboard/admin/services/add/', dashboards.service_upsert, name='service_create'),
    path('dashboard/admin/services/edit/<int:pk>/', dashboards.service_upsert, name='service_edit'),

    # Analytics / AI / Chatbot
    path('ai-measure/', ai.ai_measure, name='ai_measure'),
    path('api/process-measurement/', ai.process_measurement, name='process_measurement'),
    path('api/chatbot/', api.chatbot_api, name='chatbot_api'),
]