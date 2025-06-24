from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response  # Исправленный импорт


def home(request):
    return render(request, 'home.html')

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
