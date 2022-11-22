from django.db import models
from shop.models import Product


class Order(models.Model):
    DELIVERY_METHOD = [
        ('Самовывоз', 'Самовивозом'),
        ('Новой почтой', 'Доставка Новою почтою')
    ]

    PAYMENT_METHOD = [
        ('Наличными', 'Оплата готівкою'),
        ('Картой', 'Оплата картою'),
        ('Наложенный платеж', 'Накладеним платежем')
    ]

    name = models.CharField(max_length=50, verbose_name='Імя')
    surname = models.CharField(max_length=50, verbose_name='Прізвище')
    phone = models.CharField(max_length=20, verbose_name='Номер телефону')
    email = models.CharField(max_length=150, db_index=True, verbose_name='Email')
    delivery = models.CharField(max_length=50, choices=DELIVERY_METHOD, verbose_name='Спосіб доставки')
    address = models.CharField(max_length=150, verbose_name='Адреса або відділення НП')
    city = models.CharField(max_length=50, verbose_name='Город')
    country = models.CharField(max_length=50, verbose_name='Страна')
    post = models.CharField(max_length=10, verbose_name='Поштовий індекс')
    payment = models.CharField(max_length=50, choices=PAYMENT_METHOD, verbose_name='Спосіб оплати')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=True, verbose_name='Заказ активен?')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created', 'paid')

    def __str__(self):
        return f'Заказ №{self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products', verbose_name='Продукт')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    count = models.IntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.product.name} для заказа №{self.order.id}'

    def get_cost(self):
        return self.price * self.count
