from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=100)
    image = models.ImageField(upload_to='images/category/', verbose_name='Фотография категории')
    icon = models.ImageField(upload_to='images/category/icons/', null=True, verbose_name='Иконка категории')
    subcategory = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Категория')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        index_together = ('slug', )
        ordering = ('name', )

    def get_absolute_url(self):
        return reverse('shop:products_by_category', kwargs={'slug_category': self.slug})

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    id = models.CharField(max_length=15, primary_key=True, db_index=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=150,  verbose_name='Название детали')
    slug = models.SlugField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    is_special = models.BooleanField(default=False, verbose_name='Скидка')
    old_price = models.DecimalField(max_digits=10, blank=True, null=True, decimal_places=2, verbose_name='Старая цена')
    description = models.TextField(blank=True, verbose_name='Описание')
    remark = models.TextField(blank=True, verbose_name='Примечание')
    image = models.ImageField(upload_to=f'images/products/', verbose_name='Фотография')
    count = models.IntegerField(verbose_name='Количество на складе')
    used_quantity = models.IntegerField(verbose_name='Количество Б/У на складе')
    available = models.BooleanField(default=True, verbose_name='Наличие')
    best_seller = models.BooleanField(default=False, verbose_name='Найболее продаваемое')
    new_in = models.BooleanField(default=False, verbose_name='Новинка')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    update = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'
        index_together = ('slug', )
        ordering = ('id', 'name', '-created')

    def get_absolute_url(self):
        return reverse('shop:product', kwargs={'slug': self.slug})

    @property
    def price_percentage(self):
        return 100 * (self.old_price - self.price) / self.old_price

    def __str__(self):
        return f'{self.id} | {self.name}'


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Деталь')
    image = models.ImageField(upload_to=f'images/products/', verbose_name='Фотография')

    class Meta:
        verbose_name = 'Фотография детали'
        verbose_name_plural = 'Фотографии деталей'

    def __str__(self):
        return f'{self.product.id} - {self.id}'


class Contact(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=25, verbose_name='Телефон')
    message = models.TextField(verbose_name='Сообщения')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    is_processing = models.BooleanField(default=False, verbose_name='Ответить')

    class Meta:
        verbose_name = 'Cвяжитесь с нами'
        verbose_name_plural = 'Свзяжитесь с нами'
        ordering = ('-date', 'is_processing')

    def __str__(self):
        return f'{self.surname} {self.name} ({self.email}, {self.phone})'
