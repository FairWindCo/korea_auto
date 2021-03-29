from django.urls import path

from list_auto.views import CarListView, CarDetailView, index, CarListViewAjax

urlpatterns = [
    path('', index, name='index'),
    path('cars', CarListView.as_view(), name='car_list_view'),
    path('car_<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('ajax_cars', CarListViewAjax.as_view(), name='car_list_view_ajax'),
]
