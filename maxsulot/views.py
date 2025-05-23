from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F, Avg
from django.contrib import messages
from django.urls import reverse
from django.utils import translation

from config import settings
from .forms import ContactForm
from .models import Maxsulot, Comment, Categories
import re
import asyncio
from telegram import Bot
import httpx

# Telegram bot settings
TELEGRAM_BOT_TOKEN = '7574990859:AAEzIKl5EfIzlnIowf3N6wPCAJSeFOsQjvY'
TELEGRAM_CHAT_ID = '7126357860'

async def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    async with httpx.AsyncClient() as client:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def home(request):
    maxsulot_list = Maxsulot.objects.all().order_by('-published')
    categories = Categories.objects.all()
    paginator = Paginator(maxsulot_list, 6)
    page = request.GET.get('page')
    try:
        maxsulot = paginator.page(page)
    except PageNotAnInteger:
        maxsulot = paginator.page(1)
    except EmptyPage:
        maxsulot = paginator.page(paginator.num_pages)
    context = {
        'maxsulot': maxsulot,
        'categories': categories
    }
    return render(request, 'home.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Categories, slug=slug)
    products = category.products.all()
    paginator = Paginator(products, 9)  # Har sahifada 9 ta mahsulot
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Categories.objects.all()
    context = {
        'category': category,
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'category_detail.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Maxsulot, slug=slug)
    Maxsulot.objects.filter(slug=slug).update(views_count=F('views_count') + 1)
    comments = product.comments.all().order_by('-created_at')
    average_rating = product.comments.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    average_rating = round(average_rating, 1)

    if request.method == 'POST':
        content = request.POST.get('content')
        rating = request.POST.get('rating', 1)
        if content and rating:
            try:
                rating = int(rating)
                if 1 <= rating <= 5:
                    Comment.objects.create(
                        product=product,
                        user=request.user,
                        content=content,
                        rating=rating
                    )
                    messages.success(request, 'Your comment has been added!')
                    return redirect('product_detail', slug=slug)
                else:
                    messages.error(request, 'Rating must be between 1 and 5.')
            except ValueError:
                messages.error(request, 'Invalid rating value.')
        else:
            messages.error(request, 'Comment and rating are required.')

    context = {
        'product': product,
        'comments': comments,
        'average_rating': average_rating
    }
    return render(request, 'product_detail.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():  # TO‘G‘RI
            contact = form.save()
            messages.success(request, 'Your message has been sent successfully!')
            # Send to Telegram
            message = (
                f"New Contact Message\n"
                f"Name: {contact.name}\n"
                f"Last Name: {contact.last_name}\n"
                f"Email: {contact.email}\n"
                f"Message: {contact.message}\n"
                f"Sent at: {contact.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
            )
            try:
                asyncio.run(send_telegram_message(message))
            except Exception as e:
                messages.error(request, f"Failed to send message to Telegram: {str(e)}")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def set_language(request):
    lang_code = request.GET.get('lang', 'uz')
    translation.activate(lang_code)
    request.session['django_language'] = lang_code
    return redirect(request.META.get('HTTP_REFERER', '/'))

def all_products(request):
    maxsulot_list = Maxsulot.objects.all().order_by('-published')
    paginator = Paginator(maxsulot_list, 9)
    page_number = request.GET.get('page')
    try:
        maxsulot = paginator.page(page_number)
    except PageNotAnInteger:
        maxsulot = paginator.page(1)
    except EmptyPage:
        maxsulot = paginator.page(paginator.num_pages)
    return render(request, 'all_products.html', {'page_obj': maxsulot})

def categories(request):
    categories = Categories.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'categories.html', context)