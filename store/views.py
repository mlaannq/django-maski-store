from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework import generics
from .models import Category, Manufacturer, Product, Cart, CartItem, Order, OrderItem
from .forms import CartUpdateForm, CheckoutForm
import os
from openpyxl import Workbook
from django.core.mail import EmailMessage
from rest_framework import viewsets
from .models import Category, Manufacturer, Product, Cart, CartItem, Order, OrderItem
from .serializers import (
    CategorySerializer,
    ManufacturerSerializer,
    ProductSerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    OrderItemSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

# Базовые представления
def home(request):
    """Главная страница"""
    return render(request, 'store/home.html')

def about_author(request):
    """Страница об авторе"""
    context = {'author_name': 'Насковец Милана', 'group': '82 тп'}
    return render(request, 'store/author.html', context)

def about_store(request):
    """Страница о магазине"""
    context = {
        'store_url': 'https://maski.by/',
        'lab_theme': 'Создание и базовая настройка приложений Django',
        'store_description': 'Интернет-магазин тематических костюмов'
    }
    return render(request, 'store/store.html', context)

# API представления
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()

class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()

@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        # Обработка случая, когда корзина не существует
        return redirect('product_list')

    cart_items = cart.items.all()

    # Если корзина пуста, перенаправляем в каталог
    if not cart_items:
        return redirect('product_list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Создаем заказ
            order = Order.objects.create(
                user=request.user,
                shipping_address=form.cleaned_data['shipping_address'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone']
            )

            # Добавляем товары в заказ
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # Генерируем Excel-чек
            wb = Workbook()
            ws = wb.active
            ws.title = "Order Receipt"

            # Заголовки
            headers = ["Товар", "Количество", "Цена за единицу", "Сумма"]
            ws.append(headers)

            # Данные о товарах
            for item in order.items.all():
                ws.append([
                    item.product.name,
                    item.quantity,
                    float(item.price),
                    float(item.price * item.quantity)
                ])

            # Итоговая сумма
            total = sum(item.price * item.quantity for item in order.items.all())
            ws.append(["", "", "ИТОГО:", float(total)])

            # Сохраняем файл
            filename = f"order_{order.id}.xlsx"
            wb.save(filename)

            # Отправляем email
            subject = f"Ваш заказ #{order.id} оформлен"
            message = (
                f"Спасибо за ваш заказ!\n"
                f"Номер заказа: {order.id}\n"
                f"Дата заказа: {order.created_at.strftime('%d.%m.%Y %H:%M')}\n"
                f"Адрес доставки: {order.shipping_address}\n\n"
                f"Чек прикреплен к этому письму."
            )

            email = EmailMessage(
                subject,
                message,
                'noreply@maskistore.com',  # Замените на реальный email
                [order.email]
            )
            email.attach_file(filename)
            email.send()

            # Удаляем временный файл
            os.remove(filename)

            # Очищаем корзину
            cart.items.all().delete()

            return render(request, 'store/checkout_success.html', {'order': order})
    else:
        form = CheckoutForm()

    return render(request, 'store/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total_price': cart.total_price()
    })