from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from list_auto.models import Car


class CarListView(ListView):
    model = Car
    paginate_by = 5
    template_name = 'list_auto/car_list_tamplate.html'
