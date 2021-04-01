import os
from datetime import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views.generic import DetailView

from korea_auto import settings
from list_auto.models import Car, BodyType, Brand, CarModel
from vue_utils.utils import get_image_data, get_from_request
from vue_utils.views import FilterListView, FilterAjaxListView


class CarListViewAjax(FilterAjaxListView):
    model = Car
    paginate_by = 5
    serialized_fields = ['model_version', 'year', 'get_price', 'car_code', 'ge_thb_image',
                         'gasoline', 'mileage', 'model_version__body_type__name', 'model_version__get_engine_volume',
                         #'model_version__get_engine_volume', 'model_version__body_type',
                         'transmission__name', ]
    filters_fields = [('year', 'gte', 'start_year', 'int'),
                      ('year', 'lte', 'end_year', 'int'),
                      {
                          'field_name': 'model_version__body_type__id',
                          'field_action': 'in',
                          'form_field_name': 'body',
                          'value_as_filter': False,
                      },
                      ('model_version__model_version__brand__id', 'in', 'brand', None, False),
                      ('model_version__model_version__id', 'in', 'model', None, False),
                      ]
    # viewed_fields = [
    #     'year',
    #     {
    #         'field_name': 'model_version__body_type__id',
    #         'convertor': 'int'
    #     },
    # ]


class BrandListViewAjax(FilterAjaxListView):
    model = Brand
    viewed_fields = ['id', 'name']
    paginate_by = None
    filters_fields = [('name', "icontains", 'brand')]


class BodyTypeListViewAjax(FilterAjaxListView):
    model = BodyType
    paginate_by = None
    viewed_fields = ['id', 'name']


class ModelsListViewAjax(FilterAjaxListView):
    model = CarModel
    paginate_by = None
    filters_fields = [('brand__id', 'in', 'brand', None, False),
                      ('name', "icontains", 'model')]
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
        },
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


def search_app_index(request):
    car_body = BodyType.objects.all()
    cars = Car.objects.order_by('-created').order_by().all()[:5]
    return render(request, 'list_auto/search_app.html', {
        'car_body': car_body,
        'car_list': cars,
    })


def get_car_images_ajax(request):
    car_code = get_from_request(request, 'car_code', 0)
    dir = os.path.join(settings.MEDIA_ROOT, str(car_code))
    car_image_base_url = f'{settings.MEDIA_URL}{car_code}'
    return JsonResponse(get_image_data(dir, 'big_image_*.jpg', prepend_url=car_image_base_url), safe=False)


def get_car_additional_ajax(request):
    car_code = get_from_request(request, 'car_code', 0)
    dir = os.path.join(settings.MEDIA_ROOT, str(car_code), 'add.html')
    if os.path.exists(dir) and os.path.isfile(dir):
        with open(dir, 'r', encoding='utf-8') as file:
            content = file.read()
            pos_start = content.find('<body')
            pos_end = None
            if pos_start:
                pos_start = content.find('>', pos_start) + 1
                pos_end = content.find('</body>')

            content = content[pos_start:pos_end]
            content = content.replace('src="', f'src="/media/{car_code}/')
            content = content.replace("src='", f"src='/media/{car_code}/")
        return HttpResponse(content)
    else:
        return HttpResponse('')
