from datetime import datetime

from django.shortcuts import render
# Create your views here.
from django.views.generic import DetailView

from list_auto.models import Car, BodyType, Brand, CarModel
from vue_utils.views import FilterListView, FilterAjaxListView


class CarListViewAjax(FilterAjaxListView):
    model = Car
    paginate_by = 5
    viewed_fields = [
        'year',
        {
            'field_name': 'model_version__body_type__id',
            'convertor': 'int'
        },
    ]


class BrandListViewAjax(FilterAjaxListView):
    model = Brand
    paginate_by = 5
    viewed_fields = ['id', 'name']


class ModelsListViewAjax(FilterAjaxListView):
    model = CarModel
    paginate_by = 10
    filters_fields = [('brand__id', None)]
    viewed_fields = ['id', 'name']


class CarListView(FilterListView):
    model = Car
    paginate_by = 5
    template_name = 'list_auto/car_list_tamplate.html'
    ordering = '-created'

    filters_fields = [
        'year',
        {
            'field_name': 'model_version__body_type__id',
            'field_action': '',
            'form_field_name': 'body',
            'form_field_converter': 'int'
        },
        {
            'field_name': 'model_version__model_version__brand__id',
            'field_action': '',
            'form_field_name': 'brand',
            'form_field_converter': 'int'
        }
    ]

    def get_additional_context_attribute(self):
        return {
            'filter_year_list': [str(year) for year in range(2000, int(datetime.now().year) + 1)],
            'filter_body_list': BodyType.objects.all(),
            'filter_brand_list': Brand.objects.all(),
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
