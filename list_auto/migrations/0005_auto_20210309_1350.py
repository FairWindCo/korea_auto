# Generated by Django 3.1.7 on 2021-03-09 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_auto', '0004_auto_20210309_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='price_dealer',
            field=models.IntegerField(blank=True, null=True, verbose_name='Цена Диллера'),
        ),
        migrations.AddField(
            model_name='car',
            name='price_sale',
            field=models.IntegerField(blank=True, null=True, verbose_name='Цена Продавца'),
        ),
    ]
