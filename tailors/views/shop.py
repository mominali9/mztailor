from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from tailors.models.base_models import Category, Logo

# Shop uses models from base and shop
from tailors.models.shop_models import Product, ProductVariation, Cart, CartItem

def shop(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    logo = Logo.objects.filter(is_active=True).first()
    return render(request, 'tailors/shop.html', {
        'products': products, 
        'categories': categories,
        'logo': logo
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    variations = product.variations.all()
    logo = Logo.objects.filter(is_active=True).first()
    return render(request, 'tailors/product_detail.html', {
        'product': product,
        'variations': variations,
        'logo': logo
    })

def cart_view(request):
    logo = Logo.objects.filter(is_active=True).first()
    cart = None
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            product_id = request.POST.get('product_id')
            variation_id = request.POST.get('variation_id')
            quantity = int(request.POST.get('quantity', 1))
            
            product = get_object_or_404(Product, id=product_id)
            variation = ProductVariation.objects.filter(id=variation_id).first() if variation_id else None
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, 
                product=product,
                variation=variation,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            # --- EMAIL ADMIN ---
            from django.core.mail import send_mail
            from django.conf import settings
            try:
                msg = f"User {request.user.username if request.user.is_authenticated else 'Guest'} added {quantity}x {product.name} to their cart."
                send_mail(
                    subject='New Cart Addition',
                    message=msg,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[admin.email for admin in User.objects.filter(is_superuser=True) if admin.email],
                    fail_silently=True,
                )
            except Exception as e:
                pass # Fail silently for dev
            
            messages.success(request, f"Added {product.name} to your cart.")
            return redirect('cart')
            
        elif action == 'remove':
            item_id = request.POST.get('item_id')
            CartItem.objects.filter(id=item_id, cart=cart).delete()
            messages.success(request, "Item removed from cart.")
            return redirect('cart')
    
    total_amount = sum(item.get_total_price() for item in cart.items.all()) if cart else 0
    context = {'cart': cart, 'logo': logo, 'total_amount': total_amount}
    return render(request, 'tailors/cart.html', context)

def customizer_view(request):
    logo = Logo.objects.filter(is_active=True).first()
    return render(request, 'tailors/customizer.html', {'logo': logo})
