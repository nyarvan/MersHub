# Generated by Django 4.1.2 on 2023-06-29 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_alter_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Название детали'),
        ),
    ]