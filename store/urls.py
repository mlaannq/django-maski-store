from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views  # Импортируем весь модуль views

router = DefaultRouter()

urlpatterns = [
    path('', views.home, name='home'),
    path('author/', views.about_author, name='author'),
    path('store/', views.about_store, name='store'),
    path('checkout/', views.checkout, name='checkout'),  # Исправлено: views.checkout

    # API endpoints
    path('api/', include(router.urls)),
]