from django.urls import path

from list_auto.views import CarListView, CarDetailView, index, search_app_index

urlpatterns = [
    path('', index, name='index'),
    path('cars', CarListView.as_view(), name='car_list_view'),
    path('car_<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('search', search_app_index, name='search_app')
]
