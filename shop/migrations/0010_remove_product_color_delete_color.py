# Generated by Django 4.1.2 on 2022-11-16 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_product_old_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.DeleteModel(
            name='Color',
        ),
    ]
