# Generated by Django 4.1.2 on 2022-11-07 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name', 'subcategory'), 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
    ]
