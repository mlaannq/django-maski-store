from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'manufacturers', views.ManufacturerViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'carts', views.CartViewSet)
router.register(r'cartitems', views.CartItemViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'orderitems', views.OrderItemViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('author/', views.about_author, name='author'),
    path('store/', views.about_store, name='store'),
    path('checkout/', views.checkout, name='checkout'),  # Исправлено: views.checkout

    # API endpoints
    path('api/', include(router.urls)),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]