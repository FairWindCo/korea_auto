from django.shortcuts import render
# Create your views here.
from django.views.generic import DetailView

from list_auto.models import Car, BodyType
from vue_utils.views import FilterListView


class CarListView(FilterListView):
    model = Car
    paginate_by = 5
    template_name = 'list_auto/car_list_tamplate.html'

    def get_additional_context_attribute(self):
        return {
            'filter_year_list': [str(year) for year in range(2000, 2021)]
        }


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
