from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'spec', views.SpecialtyViewSet, basename='specialty')

urlpatterns = [
    path('qualifications/', views.qualifications_list, name='qualifications'),
    path('', views.home, name='home'),
    path('author/', views.about_author, name='author'),
    path('store/', views.about_store, name='store'),

    # API endpoints
    path('api/', include(router.urls)),
]