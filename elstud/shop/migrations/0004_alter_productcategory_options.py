# Generated by Django 4.1.7 on 2023-05-07 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_seller'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productcategory',
            options={'verbose_name': 'Категория продукта', 'verbose_name_plural': 'Категории продуктов'},
        ),
    ]