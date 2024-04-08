from django.db import models
from shop.models import Product


class Order(models.Model):
    """
    Model class representing an order.

    This model represents an order placed by a user.

    Attributes:
        DELIVERY_METHOD (list of tuples): Choices for delivery methods.
        PAYMENT_METHOD (list of tuples): Choices for payment methods.
        name (CharField): The name of the customer.
        surname (CharField): The surname of the customer.
        phone (CharField): The phone number of the customer.
        email (CharField): The email address of the customer.
        delivery (CharField): The chosen delivery method.
        address (CharField): The delivery address or post office number.
        city (CharField): The city of the customer.
        country (CharField): The country of the customer.
        post (CharField): The postal code of the delivery address.
        payment (CharField): The chosen payment method.
        created (DateTimeField): The date and time when the order was created.
        updated (DateTimeField): The date and time when the order was
    last updated.
        paid (BooleanField): Indicates whether the order is paid.

    """
    DELIVERY_METHOD = [
        ('Самовывоз', 'Самовивозом'),
        ('Новой почтой', 'Доставка Новою почтою'),
        ('Доставка', 'Доставка MERSHUB')
    ]

    PAYMENT_METHOD = [
        ('Наличными', 'Оплата готівкою'),
        ('Картой', 'Оплата картою'),
        ('Наложенный платеж', 'Накладеним платежем')
    ]

    name = models.CharField(max_length=50, verbose_name='Імя')
    surname = models.CharField(max_length=50, verbose_name='Прізвище')
    phone = models.CharField(max_length=20, verbose_name='Номер телефону')
    email = models.CharField(
        max_length=150, db_index=True, verbose_name='Email')
    delivery = models.CharField(
        max_length=50, choices=DELIVERY_METHOD, verbose_name='Спосіб доставки')
    address = models.CharField(
        max_length=150, verbose_name='Адреса або відділення НП')
    city = models.CharField(max_length=50, verbose_name='Город')
    country = models.CharField(max_length=50, verbose_name='Страна')
    post = models.CharField(max_length=10, verbose_name='Поштовий індекс')
    payment = models.CharField(
        max_length=50, choices=PAYMENT_METHOD, verbose_name='Спосіб оплати')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=True, verbose_name='Заказ активен?')

    class Meta:
        """
        Metadata class for the model.

        Attributes:
            verbose_name (str): The singular name for the model
        in the admin interface.
            verbose_name_plural (str): The plural name for the model
        in the admin interface.
            ordering (tuple): The default ordering for querysets of this model.

        """
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created', 'paid')

    def __str__(self):
        """
        Method to represent the object as a string.

        Returns:
            str: A string representation of the order.

        """
        return f'Заказ №{self.id}'

    def get_total_cost(self):
        """
        Method to calculate the total cost of the order.

        Returns:
            Decimal: The total cost of the order.

        """
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """
    Model class representing an item in an order.

    This model represents a product added to an order.

    Attributes:
        order (ForeignKey): The order to which the item belongs.
        product (ForeignKey): The product being ordered.
        price (DecimalField): The price of the product at the time
    of the order.
        count (IntegerField): The quantity of the product being ordered.

    """
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='products', verbose_name='Продукт')
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Цена')
    count = models.IntegerField(default=1, verbose_name='Количество')

    class Meta:
        """
        Metadata class for the model.

        Attributes:
            verbose_name (str): The singular name for the model
        in the admin interface.
            verbose_name_plural (str): The plural name for the model
        in the admin interface.

        """
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        """
        Method to represent the object as a string.

        Returns:
            str: A string representation of the order item.

        """
        return f'{self.product.name} для заказа №{self.order.id}'

    def get_cost(self):
        """
        Method to calculate the total cost of the order item.

        Returns:
            Decimal: The total cost of the order item.

        """
        return self.price * self.count
