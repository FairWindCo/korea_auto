# Generated by Django 3.1.7 on 2021-03-09 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('list_auto', '0003_auto_20210309_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='checkout_no',
            field=models.IntegerField(default=-1, verbose_name='CheckoutNo'),
        ),
        migrations.AddField(
            model_name='car',
            name='label_image_count',
            field=models.IntegerField(default=0, verbose_name='Кол-во флажков изображений'),
        ),
        migrations.AddField(
            model_name='car',
            name='price',
            field=models.IntegerField(default=-1, verbose_name='Цена'),
            preserve_default=False,
        ),
    ]
