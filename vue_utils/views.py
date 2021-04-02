from typing import Iterable

from django.http import Http404, JsonResponse
from django.shortcuts import render
# Create your views here.
from django.views.generic import ListView
from django.utils.translation import gettext as _

from vue_utils.utils import form_filter_dict, get_from_container, get_from_request, \
    my_serializer


def view_test(request):
    return render(request, 'vue_utils/vue_base_template.html', context={})


class FilterListView(ListView):
    """A base view for displaying a list of objects."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_defined_paging = self.paginate_by
        self.user_defined_sort = self.ordering

    # Поля для по для фильтрации с описаниями:
    # Список из:
    # str - название поля
    # dict(    'field_name' - имя поля
    #          'field_action' - действие фильтрации icontains, exact, iexact, contains, in, gt, gte, lt, lte, ....
    # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#id4
    #          'form_field_name' - имя поля в форме
    #          'form_field_converter' - преобразователь занчений формы (конвенртор)
    # )
    # tuple(   имя поля,
    #          действие фильтрации icontains, equal, ....,
    #          имя поля в форме,
    #          преобразователь занчений формы (конвенртор)
    # )
    filters_fields = None
    last_request = None
    # Метод поиска по умолчанию
    default_filter_action = 'icontains'
    # Дополнительные атрибуты которые передаются в шаблон
    additional_static_attribute = {}
    filter_form_values = {}
    # Поля для отображения (список имен)
    viewed_fields = None

    page_row_request_field = 'per_page'
    sort_request_field = 'sort_by'

    def get_additional_context_attribute(self):
        return {}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        add_context = self.get_additional_context_attribute()
        if add_context:
            context.update(**add_context)
        if self.additional_static_attribute:
            context.update(**self.additional_static_attribute)

        if self.filter_form_values:
            context.update(**{'filter_form_values': self.filter_form_values})
        return context

    def get_queryset(self):
        if self.filters_fields is None and self.model:
            self.filters_fields = [field_def.name for field_def in self.model._meta.fields]
        list_objects = super().get_queryset()

        if self.last_request and self.filters_fields:
            filter_def, self.filter_form_values = form_filter_dict(self.last_request, self.filters_fields,
                                                                   self.default_filter_action)
            self.paginate_by = get_from_request(self.last_request, self.page_row_request_field,
                                                self.user_defined_paging)
            self.ordering = get_from_request(self.last_request, self.sort_request_field,
                                             self.user_defined_sort)

            if filter_def:
                # print(filter_def, self.filter_form_values)
                list_objects = list_objects.filter(**filter_def)
            order = self.get_ordering()
            if order:
                if isinstance(order, Iterable) and not isinstance(order, str):
                    list_objects = list_objects.order_by(*order)
                else:
                    list_objects = list_objects.order_by(order)
        if self.viewed_fields:
            view_field_desc = [get_from_container(field_name, [('field_name', None)], True)[0] for field_name in
                               self.viewed_fields]
            list_objects = list_objects.values(*view_field_desc)
        return list_objects

    def get(self, request, *args, **kwargs):
        self.last_request = request
        return super(FilterListView, self).get(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        self.last_request = request
        return super(FilterListView, self).get(request, *args, *kwargs)


class FilterAjaxListView(FilterListView):
    # viewed_fields - Поля для по для отображения:
    # Список из:
    # str - название поля
    # dict(    'field_name' - имя поля
    #          'convertor' - преобразователь занчений формы (конвенртор)
    # )
    # tuple(   имя поля,
    #          преобразователь занчений формы (конвенртор)
    # )
    incorrect_page_as_empty_list = True
    serialized_fields = None
    standard_serializer = None

    def get(self, request, *args, **kwargs):
        self.last_request = request
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.

            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_('Empty list and “%(class_name)s.allow_empty” is False.') % {
                    'class_name': self.__class__.__name__,
                })
        serializer = my_serializer

        viewed_fields = None

        if self.viewed_fields is None and self.model:
            viewed_fields = [field_def.name for field_def in self.model._meta.fields]

        if self.serialized_fields is None:
            serialized_fields = viewed_fields
        else:
            serialized_fields = self.serialized_fields

        if self.standard_serializer:
            serializer = self.standard_serializer
        elif hasattr(self.model, 'serializer'):
            serializer = self.model.serializer

        page_size = self.get_paginate_by(self.object_list)

        context = {}
        if page_size:
            try:
                paginator, page, queryset, is_paginated = self.paginate_queryset(self.object_list, page_size)
                count = self.object_list.count()
                context['data_count'] = count
                context['data_list'] = page.object_list
                context['page_count'] = paginator.num_pages
                context['page'] = page.number
            except Http404 as e404:
                if self.incorrect_page_as_empty_list:
                    context['data_list'] = []
                    count = self.object_list.count()
                    context['data_count'] = count
                    context['page_count'] = count % int(page_size) + 1
                    context['page'] = get_from_request(request, 'page', 0)
                else:
                    raise e404
        else:
            context['data_list'] = self.object_list

        if serializer:
            context['data_list'] = [serializer(data_object, serialized_fields) for data_object in context['data_list']]

        add_context = self.get_additional_context_attribute()
        if add_context:
            context.update(**add_context)
        if self.additional_static_attribute:
            context.update(**self.additional_static_attribute)

        return JsonResponse(context)
