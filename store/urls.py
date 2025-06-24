from django.urls import path
from . import views  # Импортируем представления из текущего приложения

urlpatterns = [
    # Главная страница (корневой URL)
    path('', views.home, name='home'),

    # Страница "Об авторе"
    path('author/', views.about_author, name='author'),

    # Страница "О магазине"
    path('store/', views.about_store, name='store'),
]