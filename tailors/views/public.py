from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from tailors.models.base_models import Article, Service, Testimonial, Category, Video, Logo, Statistics
from tailors.forms import ContactForm, TestimonialForm

def home(request):
    articles = Article.objects.filter(is_published=True)[:3]
    services = Service.objects.filter(is_active=True)[:6]
    testimonials = Testimonial.objects.filter(is_approved=True)[:3]
    categories = Category.objects.filter(is_active=True)[:8]
    videos = Video.objects.filter(is_active=True).first()
    logo = Logo.objects.filter(is_active=True).first()
    stats = Statistics.objects.filter(is_active=True).first()
    
    context = {
        'articles': articles,
        'services': services,
        'testimonials': testimonials,
        'categories': categories,
        'videos': videos,
        'logo': logo,
        'stats': stats,
    }
    return render(request, 'tailors/home.html', context)

def articles_list(request):
    articles = Article.objects.filter(is_published=True)
    logo = Logo.objects.filter(is_active=True).first()
    return render(request, 'tailors/articles.html', {'articles': articles, 'logo': logo})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk, is_published=True)
    logo = Logo.objects.filter(is_active=True).first()
    return render(request, 'tailors/article_detail.html', {'article': article, 'logo': logo})

def services(request):
    services = Service.objects.filter(is_active=True)
    logo = Logo.objects.filter(is_active=True).first()
    return render(request, 'tailors/services.html', {'services': services, 'logo': logo})

def about(request):
    logo = Logo.objects.filter(is_active=True).first()
    return render(request, 'tailors/about.html', {'logo': logo})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    logo = Logo.objects.filter(is_active=True).first()
    return render(request, 'tailors/contact.html', {'form': form, 'logo': logo})

def feedback(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your feedback! It will be reviewed and published soon.')
            return redirect('feedback')
    else:
        form = TestimonialForm()
    
    logo = Logo.objects.filter(is_active=True).first()
    return render(request, 'tailors/feedback.html', {'form': form, 'logo': logo})
