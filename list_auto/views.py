from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView

from list_auto.models import Car, BodyType


class CarListView(ListView):
    model = Car
    paginate_by = 5
    template_name = 'list_auto/car_list_tamplate.html'


class CarDetailView(DetailView):
    model = Car
    template_name = 'list_auto/car_detail_template.html'


def index(request):
    car_body = BodyType.objects.all()
    cars = Car.objects.order_by('-created').order_by().all()[:5]
    return render(request, 'list_auto/car_index_template.html', {
        'car_body': car_body,
        'car_list': cars,
    })