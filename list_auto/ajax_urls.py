from django.urls import path

from list_auto.views import CarListViewAjax, BrandListViewAjax, ModelsListViewAjax, BodyTypeListViewAjax, \
    get_car_images_ajax, get_car_additional_ajax

urlpatterns = [
    path('cars', CarListViewAjax.as_view(), name='car_list_ajax'),
    path('brands', BrandListViewAjax.as_view(), name='brand_list_ajax'),
    path('bodytypes', BodyTypeListViewAjax.as_view(), name='body_list_ajax'),
    path('models', ModelsListViewAjax.as_view(), name='models_list_ajax'),
    path('images', get_car_images_ajax, name='images_ajax'),
    path('additional', get_car_additional_ajax, name='additional_ajax'),
]
