from select import select

from django.db import models


# Create your models here.
class Brand(models.Model):
    name = models.CharField(verbose_name='Название бренда', max_length=50)
    korea_name = models.CharField(verbose_name='Корейское название бренда', max_length=100)
    code = models.IntegerField(verbose_name='Код на корейском сайте')

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


# Create your models here.
class CarModel(models.Model):
    name = models.CharField(verbose_name='Модель', max_length=50)
    korea_name = models.CharField(verbose_name='Корейское название модели', max_length=100)
    code = models.IntegerField(verbose_name='Код на корейском сайте')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'

    def __str__(self):
        return f'{self.brand.name} {self.name}'


class BodyType(models.Model):
    name = models.CharField(verbose_name='Тип кузова', max_length=50)
    class Meta:
        verbose_name = 'Тип кузова'
        verbose_name_plural = 'Типы кузова'

    def __str__(self):
        return f'{self.name}'

class CarVersion(models.Model):
    name = models.CharField(verbose_name='Версия модели', max_length=50)
    korea_name = models.CharField(verbose_name='Корейское название модели', max_length=100)
    code = models.IntegerField(verbose_name='Код на корейском сайте')
    model_version = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    engine_volume = models.IntegerField(verbose_name='Объем двигателя', null=True, blank=True, max_length=2)
    four_wd = models.BooleanField(verbose_name='4WD', null=True, blank=True)
    body_type = models.ForeignKey(BodyType, on_delete=models.CASCADE, verbose_name='Тип кузова', blank=True, null=True)

    class Meta:
        verbose_name = 'Версия Модели'
        verbose_name_plural = 'Версия Модели'

    def __str__(self):
        return f'{self.model_version} {self.name}'

    def get_engine_volume(self):
        return f'{self.engine_volume/10:.1f}' if self.engine_volume is not None else None


class CarOptions(models.Model):
    name = models.CharField(verbose_name='Опция', max_length=50)
    korea_name = models.CharField(verbose_name='Корейское название', max_length=100)
    code = models.IntegerField(verbose_name='Код на корейском сайте')
    option_group = models.IntegerField(verbose_name='Код гурппы опций', default=0)

    class Meta:
        verbose_name = 'Опиция'
        verbose_name_plural = 'Опции'

    def __str__(self):
        return self.name


# Create your models here.
class TransmissionsType(models.Model):
    name = models.CharField(verbose_name='Тип трансмисии', max_length=20)
    korea_name = models.CharField(verbose_name='Корейское название типа', max_length=40)
    code = models.IntegerField(verbose_name='Код на корейском сайте')

    class Meta:
        verbose_name = 'Трансмисия'
        verbose_name_plural = 'Трансмисии'

    def __str__(self):
        return self.name


# Create your models here.
class Color(models.Model):
    name = models.CharField(verbose_name='Название цвета', max_length=50)
    korea_name = models.CharField(verbose_name='Корейкое название цвета', max_length=100)
    code = models.IntegerField(verbose_name='Код на корейском сайте')

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвет'

    def __str__(self):
        return self.name


class GasolineType(models.Model):
    name = models.CharField(verbose_name='Название типа топлива', max_length=20)
    korea_name = models.CharField(verbose_name='Корейское название топлива', max_length=40)
    code = models.IntegerField(verbose_name='Код на корейском сайте')

    class Meta:
        verbose_name = 'Тип топлива'
        verbose_name_plural = 'Типы топлива'

    def __str__(self):
        return self.name


class Car(models.Model):
    car_code = models.IntegerField(verbose_name='Код на сайте')
    model_version = models.ForeignKey(CarVersion, on_delete=models.CASCADE, verbose_name='Версия модели')
    gasoline = models.ForeignKey(GasolineType, on_delete=models.CASCADE, verbose_name='Тип топлива')
    transmission = models.ForeignKey(TransmissionsType, on_delete=models.CASCADE, verbose_name='Трансмисия')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name='Цвет')
    options = models.ManyToManyField(CarOptions, verbose_name='Опции')
    year = models.IntegerField(verbose_name='Год выпуска')
    image_count = models.IntegerField(default=0, verbose_name='Кол-во изображений')
    car_LPG_use = models.BooleanField(default=False, verbose_name='Испольузет ГАЗ')
    plate_number = models.CharField(verbose_name='Номерной знак', max_length=15)
    vin_number = models.CharField(verbose_name='VIN CODE', max_length=25)
    mileage = models.IntegerField(default=0, verbose_name='Пробег')
    jesi_no = models.IntegerField(default=0, verbose_name='JESI site code')
    first_register_date = models.DateField(verbose_name='Дата первой регистации', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    checkout_no = models.IntegerField(default=-1, verbose_name='CheckoutNo')
    label_image_count = models.IntegerField(default=0, verbose_name='Кол-во флажков изображений')
    price = models.IntegerField(verbose_name='Цена')
    price_dealer = models.IntegerField(verbose_name='Цена Диллера', blank=True, null=True)
    price_sale = models.IntegerField(verbose_name='Цена Продавца', blank=True, null=True)
    lot_register_date = models.DateField(verbose_name='Дата создания лота', blank=True, null=True)
    created = models.DateTimeField(auto_created=True, verbose_name='Дата добавления в БД')
    car_smear = models.BooleanField(default=None, verbose_name='Наличие пятен', blank=True, null=True)
    car_transformation = models.BooleanField(default=None, verbose_name='Наличие модификаций (изменений)', blank=True,
                                             null=True)

    def __str__(self):
        return f'[{self.car_code}] {self.model_version}'

    def get_price(self):
        return (self.price if self.price>0 else self.price_dealer) * 1000

    def get_image_range(self):
        return range(1, self.image_count+1)

    def get_car_images(self):
        return [ f'{self.car_code}/big_image_{i}.jpg' for i in self.get_image_range()]

    def get_option(self):
        return self.options.order_by('option_group', 'name').iterator()