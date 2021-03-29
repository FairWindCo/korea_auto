from django.http import Http404, JsonResponse
from django.shortcuts import render
# Create your views here.
from django.views.generic import ListView
from importlib._common import _

from vue_utils.utils import form_filter_dict, get_from_container, standard_value_converter


def view_test(request):
    return render(request, 'vue_utils/vue_base_template.html', context={})


class FilterListView(ListView):
    """A base view for displaying a list of objects."""
    # Поля для по для фильтрации с описаниями:
    # Список из:
    # str - название поля
    # dict(    'field_name' - имя поля
    #          'field_action' - действие фильтрации icontains, equal, ....
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
    viewed_fields = []

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
            if filter_def:
                print(filter_def, self.filter_form_values)
                list_objects = list_objects.filter(**filter_def)
        if self.viewed_fields:
            view_field_desc = [get_from_container(field_name, [('field_name', None)], True)[0] for field_name in self.viewed_fields]
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
    def standard_serializer(self, current_obj):
        if self.viewed_fields is None and self.model:
            self.viewed_fields = [field_def.name for field_def in self.model._meta.fields]
        result = {}

        for field_desc in self.viewed_fields:
            field_name, convertor = get_from_container(field_desc, [
                        ('field_name', None),
                        ('convertor', None)
                    ], True)
            current_val = None
            if hasattr(current_obj, field_name):
                current_val = getattr(current_obj,field_name)
            elif field_name in current_obj:
                current_val = current_obj[field_name]
            if current_val:
                result[field_name] = standard_value_converter(current_val, convertor, False, True)
            else:
                result[field_name] = None
        return result

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
        serializer = self.standard_serializer
        if hasattr(self.model, 'serializer'):
            serializer = self.model.serializer

        page_size = self.get_paginate_by(self.object_list)

        context = {}
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(self.object_list, page_size)
            context['data_list'] = page.object_list
            context['page_count'] = paginator.num_pages
            context['page'] = page.number
        else:
            context['data_list'] = self.object_list

        if serializer:
            context['data_list'] = [serializer(data_object) for data_object in context['data_list']]

        add_context = self.get_additional_context_attribute()
        if add_context:
            context.update(**add_context)
        if self.additional_static_attribute:
            context.update(**self.additional_static_attribute)

        return JsonResponse(context)
