from django.urls import path

from list_auto.views import CarListViewAjax, BrandListViewAjax, ModelsListViewAjax

urlpatterns = [
    path('cars', CarListViewAjax.as_view(), name='car_list_ajax'),
    path('brands', BrandListViewAjax.as_view(), name='brand_list_ajax'),
    path('models', ModelsListViewAjax.as_view(), name='models_list_ajax'),
]
