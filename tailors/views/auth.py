from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib import messages
from tailors.models.base_models import Logo

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
        
    logo = Logo.objects.filter(is_active=True).first()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Default all new signups to 'Customer' role
            customer_group, _ = Group.objects.get_or_create(name='Customer')
            user.groups.add(customer_group)
            
            login(request, user)
            messages.success(request, 'Registration successful. Welcome to MZ Tailors!')
            return redirect('dashboard_redirect')
    else:
        form = UserCreationForm()
        
    return render(request, 'tailors/auth/register.html', {'form': form, 'logo': logo})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')
        
    logo = Logo.objects.filter(is_active=True).first()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard_redirect')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
        
    return render(request, 'tailors/auth/login.html', {'form': form, 'logo': logo})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')
