from django.contrib import admin

# Register your models here.
from list_auto.models import Car, GasolineType, Color, TransmissionsType, CarOptions, CarVersion, CarModel, Brand

admin.site.register(Car)
admin.site.register(GasolineType)
admin.site.register(Color)
admin.site.register(TransmissionsType)
admin.site.register(CarOptions)
admin.site.register(CarVersion)
admin.site.register(CarModel)
admin.site.register(Brand)