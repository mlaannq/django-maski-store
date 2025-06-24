from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    country = models.CharField(max_length=100, verbose_name='Страна')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    # Добавляем blank=True и null=True для необязательных изображений
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name='Фото товара'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Цена'
    )
    stock = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name='Количество на складе'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',  # Добавляем related_name
        verbose_name='Категория'
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name='products',  # Добавляем related_name
        verbose_name='Производитель'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',  # Добавляем related_name
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    def total_price(self):
        # Исправляем обработку пустой корзины
        items = self.items.all()
        return sum(item.item_price() for item in items) if items else 0

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',  # Изменяем related_name для более ясного доступа
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        default=1,  # Добавляем значение по умолчанию
        verbose_name='Количество'
    )

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"

    def item_price(self):
        return self.product.price * self.quantity

    def clean(self):
        """Валидация количества товара"""
        if self.quantity > self.product.stock:
            raise ValidationError('Недостаточно товара на складе')

    def save(self, *args, **kwargs):
        """Переопределяем save для автоматической валидации"""
        self.full_clean()  # Вызываем валидацию перед сохранением
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        # Добавляем уникальность комбинации корзины и товара
        unique_together = ('cart', 'product')

    # В самый конец models.py добавьте:
    class Specialty(models.Model):
        """Временная заглушка для старых импортов"""
        name = models.CharField(max_length=100)

        class Meta:
            managed = False  # Не создавать таблицу в БД

        def __str__(self):
            return self.name