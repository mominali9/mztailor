from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from tailors.models.base_models import Logo, Category, Service
from tailors.models.shop_models import Product, ProductVariation
from tailors.models.orders_models import Order

@login_required
def dashboard_redirect(request):
    """Routes the user to their specific dashboard based on their role."""
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    elif request.user.groups.filter(name='Employee').exists():
        return redirect('employee_dashboard')
    else:
        return redirect('customer_dashboard')

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
        
    logo = Logo.objects.filter(is_active=True).first()
    orders = Order.objects.all().order_by('-created_at')
    
    # Simple aggregates
    total_revenue = sum(o.total_amount for o in orders if o.status not in ['Pending Payment', 'Cancelled'])
    context = {
        'logo': logo,
        'orders': orders,
        'total_revenue': total_revenue,
        'in_progress_count': orders.filter(status='In Progress').count(),
        'completed_count': orders.filter(status='Completed').count()
    }
    return render(request, 'tailors/dashboards/admin.html', context)

@login_required
def employee_dashboard(request):
    if not request.user.groups.filter(name='Employee').exists() and not request.user.is_superuser:
        return redirect('dashboard_redirect')
        
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('new_status')
        if order_id and new_status:
            order = Order.objects.filter(id=order_id).first()
            if order:
                order.status = new_status
                order.save()
        return redirect('employee_dashboard')

    logo = Logo.objects.filter(is_active=True).first()
    # Employees only see orders they can work on
    active_orders = Order.objects.filter(status__in=['Paid', 'In Progress']).order_by('created_at')
    
    return render(request, 'tailors/dashboards/employee.html', {'logo': logo, 'active_orders': active_orders})


@login_required
def customer_dashboard(request):
    logo = Logo.objects.filter(is_active=True).first()
    my_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'tailors/dashboards/customer.html', {'logo': logo, 'orders': my_orders})

# --- Custom Admin Management (CRUD) ---

@login_required
def manage_products(request):
    if not request.user.is_superuser: return redirect('home')
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'tailors/dashboards/management/product_list.html', {'products': products})

@login_required
def product_upsert(request, pk=None):
    if not request.user.is_superuser: return redirect('home')
    product = get_object_or_404(Product, pk=pk) if pk else None
    
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        
        if product:
            product.name = name
            product.price = price
            product.category_id = category_id
            product.description = description
            if request.FILES.get('image'): product.image = request.FILES.get('image')
            product.save()
            messages.success(request, f"Product '{name}' updated successfully.")
        else:
            Product.objects.create(
                name=name, price=price, category_id=category_id, 
                description=description, image=request.FILES.get('image')
            )
            messages.success(request, f"Product '{name}' created successfully.")
        return redirect('manage_products')

    categories = Category.objects.all()
    return render(request, 'tailors/dashboards/management/product_form.html', {
        'product': product, 'categories': categories
    })

@login_required
def product_delete(request, pk):
    if not request.user.is_superuser: return redirect('home')
    product = get_object_or_404(Product, pk=pk)
    name = product.name
    product.delete()
    messages.success(request, f"Product '{name}' deleted.")
    return redirect('manage_products')

# Similar for Categories and Services...
@login_required
def manage_categories(request):
    if not request.user.is_superuser: return redirect('home')
    categories = Category.objects.all().order_by('order')
    return render(request, 'tailors/dashboards/management/category_list.html', {'categories': categories})

@login_required
def category_upsert(request, pk=None):
    if not request.user.is_superuser: return redirect('home')
    category = get_object_or_404(Category, pk=pk) if pk else None
    if request.method == 'POST':
        name = request.POST.get('name')
        if category:
            category.name = name
            category.description = request.POST.get('description')
            if request.FILES.get('image'): category.image = request.FILES.get('image')
            category.save()
        else:
            Category.objects.create(name=name, description=request.POST.get('description'), image=request.FILES.get('image'))
        return redirect('manage_categories')
    return render(request, 'tailors/dashboards/management/category_form.html', {'category': category})

@login_required
def manage_services(request):
    if not request.user.is_superuser: return redirect('home')
    services = Service.objects.all()
    return render(request, 'tailors/dashboards/management/service_list.html', {'services': services})

@login_required
def service_upsert(request, pk=None):
    if not request.user.is_superuser: return redirect('home')
    service = get_object_or_404(Service, pk=pk) if pk else None
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        if service:
            service.name = name
            service.price = price
            service.description = request.POST.get('description')
            service.save()
        else:
            Service.objects.create(name=name, price=price, description=request.POST.get('description'))
        return redirect('manage_services')
    return render(request, 'tailors/dashboards/management/service_form.html', {'service': service})
