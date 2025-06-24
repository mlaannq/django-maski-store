from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework import generics
from .models import Category, Manufacturer, Product, Cart, CartItem
from .forms import CartUpdateForm  # Исправленный импорт

# API представления
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()

class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
# Обычные представления
def home(request):
    return render(request, 'store/home.html')

def about_author(request):
    context = {'author_name': 'Насковец Милана', 'group': '82 тп'}
    return render(request, 'author.html', context)

def about_store(request):
    context = {
        'store_url': 'https://maski.by/',
        'lab_theme': 'Создание и базовая настройка приложений Django',
        'store_description': 'Интернет-магазин тематичских костюмов'
    }
    return render(request, 'store.html', context)

# Добавьте остальные представления (product_list, product_detail, и т.д.) из предыдущих заданий

def about_author(request):
    context = {'author_name': 'Насковец Милана', 'group': '82 тп'}
    return render(request, 'author.html', context)
def qualifications_list(request):
    """Страница с квалификациями для пользователей"""

def about_store(request):
    context = {
        'store_url': 'https://maski.by/',
        'lab_theme': 'Создание и базовая настройка приложений Django',
        'store_description': 'Интернет-магазин тематичских костюмов'
    }
    return render(request, 'store.html', context)
