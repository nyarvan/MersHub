# Generated by Django 4.1.2 on 2022-11-03 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Название категории')),
                ('slug', models.SlugField(max_length=100)),
                ('image', models.ImageField(upload_to='images/category/', verbose_name='Фотография категории')),
                ('subcategory', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('name',),
                'index_together': {('slug',)},
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=25, verbose_name='Название')),
                ('value', models.IntegerField()),
                ('css_tag', models.CharField(default='#fff', max_length=15)),
            ],
            options={
                'verbose_name': 'Цвет',
                'verbose_name_plural': 'Цвета',
                'ordering': ('value',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.IntegerField(db_index=True, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=150, verbose_name='Название детали')),
                ('slug', models.SlugField(max_length=150)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('is_special', models.BooleanField(default=False, verbose_name='Скидка')),
                ('old_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Старая цена')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('remark', models.TextField(blank=True, verbose_name='Примечание')),
                ('image', models.ImageField(upload_to='images/products/', verbose_name='Фотография')),
                ('count', models.IntegerField(verbose_name='Количество на складе')),
                ('used_quantity', models.IntegerField(verbose_name='Количество Б/У на складе')),
                ('available', models.BooleanField(default=True, verbose_name='Наличие')),
                ('best_seller', models.BooleanField(default=False, verbose_name='Найболее продаваемое')),
                ('new_in', models.BooleanField(default=False, verbose_name='Новинка')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category', verbose_name='Категория')),
                ('color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.color', verbose_name='Цвет')),
            ],
            options={
                'verbose_name': 'Деталь',
                'verbose_name_plural': 'Детали',
                'ordering': ('id', 'name', '-created'),
                'index_together': {('slug',)},
            },
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/products/', verbose_name='Фотография')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Деталь')),
            ],
            options={
                'verbose_name': 'Фотография детали',
                'verbose_name_plural': 'Фотографии деталей',
            },
        ),
    ]
