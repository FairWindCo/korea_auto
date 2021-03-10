from django.urls import path

from list_auto.views import CarListView

urlpatterns = [
    path('', CarListView.as_view(), name='car_list_view'),
]
