from django.db import models
from django.urls import reverse


class Category(models.Model):
    """
    Model class representing a category.

    This model represents a category in the system. It contains information
    such as the category name, slug, image, icon, and subcategory relationship.

    Attributes:
        name (CharField): The name of the category.
        slug (SlugField): The slug for the category URL.
        image (ImageField): The image representing the category.
        icon (ImageField): The icon representing the category.
        subcategory (ForeignKey): The parent category of the current category.

    Methods:
        get_absolute_url: Returns the absolute URL
    for the category detail view.

    """
    name = models.CharField(
        max_length=100, db_index=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=100)
    image = models.ImageField(
        upload_to='images/category/', verbose_name='Фотография категории')
    icon = models.ImageField(
        upload_to='images/category/icons/', blank=True,
        null=True, verbose_name='Иконка категории')
    subcategory = models.ForeignKey(
        'Category', on_delete=models.CASCADE,
        null=True, blank=True, verbose_name='Категория')

    class Meta:
        """
        Metadata options for the Category model.

        Attributes:
            verbose_name (str): The human-readable name for the model
        in singular form.
            verbose_name_plural (str): The human-readable name for the model
        in plural form.
            index_together (tuple): A tuple of field names
        that should be indexed together.
            ordering (list): A list of field names used
        for default ordering of querysets.

        """
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        index_together = ('slug', )
        ordering = ('name', )

    def get_absolute_url(self):
        """
        Get the absolute URL of the category.

        Returns:
            str: The absolute URL of the category.
        """
        return reverse(
            'shop:products_by_category', kwargs={'slug_category': self.slug})

    def __str__(self):
        """
        Return the string representation of the category.

        Returns:
            str: The name of the category.
        """
        return f'{self.name}'


class Product(models.Model):
    """
    Model class representing a product.

    This model represents a product in the system. It contains information
    such as the product ID, category, name, price, and availability.

    Attributes:
        id (CharField): The unique identifier for the product.
        category (ForeignKey): The category to which the product belongs.
        name (CharField): The name of the product.
        slug (SlugField): The slug for the product URL.
        price (DecimalField): The price of the product.
        is_special (BooleanField): Indicates if the product is
    on special offer.
        is_used (BooleanField): Indicates if the product is used.
        description (TextField): The description of the product.
        remark (TextField): Additional remarks for the product.
        image (ImageField): The image representing the product.
        count (IntegerField): The quantity of the product in stock.
        used_quantity (IntegerField): The quantity of used product in stock.
        available (BooleanField): Indicates if the product is available
    for purchase.
        best_seller (BooleanField): Indicates if the product is a best seller.
        new_in (BooleanField): Indicates if the product is newly added
    to the inventory.
        created (DateTimeField): The date and time the product was created.
        update (DateTimeField): The date and time the product was last updated.

    Methods:
        get_absolute_url: Returns the absolute URL for the product detail view.
        price_percentage: Calculates the percentage discount of the product.

    """
    id = models.CharField(
        max_length=35, primary_key=True, db_index=True, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(
        null=True, blank=True, max_length=150, verbose_name='Название детали')
    slug = models.SlugField(max_length=150)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Цена')
    is_special = models.BooleanField(default=False, verbose_name='Скидка')
    is_used = models.BooleanField(default=False, verbose_name='Б/У')
    old_price = models.DecimalField(
        max_digits=10, blank=True,
        null=True, decimal_places=2, verbose_name='Старая цена')
    description = models.TextField(blank=True, verbose_name='Описание')
    remark = models.TextField(blank=True, verbose_name='Примечание')
    image = models.ImageField(
        upload_to='images/products/', verbose_name='Фотография',
        default='images/products/no-image.png')
    count = models.IntegerField(verbose_name='Количество на складе')
    used_quantity = models.IntegerField(
        null=True, verbose_name='Количество Б/У на складе')
    available = models.BooleanField(default=True, verbose_name='Наличие')
    best_seller = models.BooleanField(
        default=False, verbose_name='Найболее продаваемое')
    new_in = models.BooleanField(default=False, verbose_name='Новинка')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    update = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        """
        Metadata options for the Product model.

        Attributes:
            verbose_name (str): The human-readable name for the model
        in singular form.
            verbose_name_plural (str): The human-readable name for the model
        in plural form.
            index_together (tuple): A tuple of field names that should be
        indexed together.
            ordering (list): A list of field names used
        for default ordering of querysets.

        """
        verbose_name = 'Деталь'
        verbose_name_plural = 'Детали'
        index_together = ('slug', )
        ordering = ('id', 'name', '-created')

    def get_absolute_url(self):
        """
        Get the absolute URL of the product.

        Returns:
            str: The absolute URL of the product.
        """
        return reverse('shop:product', kwargs={'slug': self.slug})

    @property
    def price_percentage(self):
        """
        Calculate the percentage discount of the product.

        Returns:
            float: The percentage discount of the product.
        """
        return 100 * (self.old_price - self.price) / self.old_price

    def __str__(self):
        """
        Return the string representation of the product.

        Returns:
            str: The string representation of the product.
        """
        return f'{self.id} | {self.name}'


class ProductImages(models.Model):
    """
    Model class representing product images.

    This model represents images associated with a product.

    Attributes:
        product (ForeignKey): The product to which the image belongs.
        image (ImageField): The image file.

    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Деталь')
    image = models.ImageField(
        upload_to='images/products/', verbose_name='Фотография')

    class Meta:
        """
        Metadata options for the ProductImages model.

        Attributes:
            verbose_name (str): The human-readable name for the model
        in singular form.
            verbose_name_plural (str): The human-readable name for the model
        in plural form.

        """
        verbose_name = 'Фотография детали'
        verbose_name_plural = 'Фотографии деталей'

    def __str__(self):
        """
        Return the string representation of the product image.

        Returns:
            str: The string representation of the product image.
        """
        return f'{self.product.id} - {self.id}'


class Contact(models.Model):
    """
    Model class representing contact information.

    This model represents contact information submitted by users.

    Attributes:
        name (CharField): The user's name.
        surname (CharField): The user's surname.
        email (EmailField): The user's email address.
        phone (CharField): The user's phone number.
        message (TextField): The message sent by the user.
        date (DateTimeField): The date and time the contact was submitted.
        is_processing (BooleanField): Indicates if the contact
    has been processed.

    """

    name = models.CharField(max_length=50, verbose_name='Имя')
    surname = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=25, verbose_name='Телефон')
    message = models.TextField(verbose_name='Сообщения')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    is_processing = models.BooleanField(default=False, verbose_name='Ответить')

    class Meta:
        """
        Metadata options for the Contact model.

        Attributes:
            verbose_name (str): The human-readable name for the model
        in singular form.
            verbose_name_plural (str): The human-readable name for the model
        in plural form.
            ordering (tuple): The default ordering of instances in querysets.

        """
        verbose_name = 'Cвяжитесь с нами'
        verbose_name_plural = 'Свзяжитесь с нами'
        ordering = ('-date', 'is_processing')

    def __str__(self):
        """
        Return the string representation of the contact information.

        Returns:
            str: A formatted string containing the user's name, surname,
        email, and phone number.
        """
        return f'{self.surname} {self.name} ({self.email}, {self.phone})'
