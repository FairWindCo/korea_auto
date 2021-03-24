from typing import Iterable, Dict, Tuple, List

from django.core import serializers
from django.core.paginator import Paginator


def get_from_request(request, request_param_name, default_value=None, raise_exception=False):
    if request_param_name and request:
        if request.GET and request_param_name in request.GET:
            return request.GET.get(request_param_name)
        elif request.POST and request_param_name in request.POST:
            return request.POST.get(request_param_name)
        elif raise_exception:
            raise ValueError(f'Param {request_param_name} not found in request')
        else:
            return default_value
    else:
        return None


def todict(obj, classkey=None):
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, classkey)
        return data
    elif hasattr(obj, "_ast"):
        return todict(obj._ast())
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value, classkey))
                     for key, value in obj.__dict__.items()
                     if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj


def standart_serializer(list_object):
    return serializers.serialize('json', list_object)


def dict_serializer(list_object):
    return [todict(obj) for obj in list_object]


def process_paging(request, objects, default_page_size='25', serializer=dict_serializer):
    page_number = get_from_request(request, 'page', '0')
    page_size = get_from_request(request, 'per_page', default_page_size)
    paginator = Paginator(objects, page_size)

    return {
        'list': serializer(paginator.get_page(page_number).object_list),
        'page_number': page_number,
        'per_page': page_size,
        'count': paginator.count
    }


def get_from_container(container, field_list_with_default_values: List[Tuple[str, any]], use_container_as_value=False):
    result = []
    if isinstance(container, str) and use_container_as_value:
        result = [def_value for field_name, def_value in field_list_with_default_values]
        result[0] = container
    elif isinstance(container, Dict):
        for field_name, def_value in field_list_with_default_values:
            result.append(container.get(field_name, def_value))
    elif isinstance(container, Iterable):
        result = [def_value for field_name, def_value in field_list_with_default_values]
        for index, value_for_field in enumerate(container[:len(result)]):
            result[index] = value_for_field
    elif use_container_as_value:
        result = [def_value for field_name, def_value in field_list_with_default_values]
        result[0] = container
    else:
        result = None
    return result


def form_filter_dict(request, filter_list, default_filter_action='icontains'):
    if filter_list:
        filter_dict = {}
        form_values = {}
        form_field_converter = None
        for filter_field_name in filter_list:
            current_field = None
            form_field_name = None
            filter_action = None
            if isinstance(filter_field_name, str):
                value = get_from_request(request, filter_field_name)
                current_field = filter_field_name
                filter_action = default_filter_action

            elif isinstance(filter_field_name, Dict) or isinstance(filter_field_name, Iterable):
                if 'field_name' in filter_field_name:
                    current_field, filter_action, form_field_name, form_field_converter = get_from_container(filter_field_name, [
                        ('field_name', None),
                        ('field_action', default_filter_action),
                        ('form_field_name', None),
                        ('form_field_converter', None),
                    ])
            if form_field_name is None:
                form_field_name = current_field

            value = get_from_request(request, form_field_name)
            if current_field and value:
                if not isinstance(value, str) and isinstance(value, Dict) or isinstance(value, Iterable):
                    current_value, filter_action = get_from_container(value,[
                        ('value', None),
                        ('action', filter_action)
                    ], True)
                else:
                    current_value = value
                if current_value is not None and form_field_converter:
                    try:
                        if callable(form_field_converter):
                            current_value = form_field_converter(current_value)
                        elif isinstance(form_field_converter, str):
                            if form_field_converter == 'int':
                                current_value = int(current_value)
                            elif form_field_converter == 'float':
                                current_value = float(current_value)
                            else:
                                current_value = str(current_value)
                    except ValueError:
                        print('Convert value error')
                        pass
                if current_value:
                    if filter_action:
                        filter_dict[f'{current_field}__{filter_action}'] = current_value
                    else:
                        filter_dict[f'{current_field}'] = current_value
                    form_values[form_field_name] = current_value

        return filter_dict, form_values
    else:
        return None, None
