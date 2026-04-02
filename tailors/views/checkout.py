import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from tailors.models.base_models import Logo
from tailors.models.shop_models import Cart
from tailors.models.orders_models import Order, OrderItem

# In a real app, define these in settings.py. For now we use standard test keys or fallback
stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', 'sk_test_123456789')

def checkout_view(request):
    logo = Logo.objects.filter(is_active=True).first()
    cart = None
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
        
    total_amount = sum(item.get_total_price() for item in cart.items.all()) if cart else 0
    
    if request.method == 'POST':
        # Create the Order Record in database
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            total_amount=total_amount,
            status='Pending Payment'
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                variation=item.variation,
                quantity=item.quantity,
                price_at_purchase=item.product.price
            )
            
        # Build Stripe Checkout Session
        # In a real app we construct exact line items
        domain_url = request.build_absolute_uri('/')[:-1]
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'gbp',
                            'unit_amount': int(total_amount * 100),
                            'product_data': {
                                'name': 'MZ Tailors Order',
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=domain_url + reverse('payment_success') + "?session_id={CHECKOUT_SESSION_ID}&order_id=" + str(order.id),
                cancel_url=domain_url + reverse('cart'),
            )
            order.stripe_checkout_id = checkout_session.id
            order.save()
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return render(request, 'tailors/checkout.html', {'cart': cart, 'logo': logo, 'total_amount': total_amount, 'error': str(e)})

    return render(request, 'tailors/checkout.html', {'cart': cart, 'logo': logo, 'total_amount': total_amount})

def payment_success(request):
    order_id = request.GET.get('order_id')
    if order_id:
        order = get_object_or_404(Order, id=order_id)
        order.status = 'Paid'
        order.save()
        
        # Clear Cart
        if request.user.is_authenticated:
            Cart.objects.filter(user=request.user).delete()
        else:
            Cart.objects.filter(session_key=request.session.session_key).delete()
            
    return render(request, 'tailors/dashboards/customer.html', {'messages': ['Payment successful! Your order is now paid.']})
