from django.shortcuts import render

def home(request):
    """Главная страница магазина"""
    return render(request, 'home.html')

def about_author(request):
    """Страница с информацией об авторе"""
    context = {
        'author_name': 'Насковец Милана',
        'group': '82 тп'
    }
    return render(request, 'author.html', context)

def about_store(request):
    """Страница с информацией о магазине и теме лабораторной"""
    context = {
        'store_url': 'https://maski.by/',      # Ссылка на референс-сайт
        'lab_theme': 'Создание и базовая настройка приложений Django',
        'store_description': 'Интернет-магазин тематичских костюмов'  # Описание магазина
    }
    return render(request, 'store.html', context)