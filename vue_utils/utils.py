import collections
import glob
import os
from typing import Iterable, Dict, Tuple, List

from PIL import Image
from django.core import serializers
from django.core.paginator import Paginator


def get_from_request(request, request_param_name, default_value=None, raise_exception=False):
    if request_param_name and request:
        if request.GET and request_param_name in request.GET:
            return request.GET.get(request_param_name)
        elif request.POST and request_param_name in request.POST:
            return request.POST.get(request_param_name)
        elif not request_param_name.endswith('[]'):
            request_param_name = request_param_name + '[]'
            if request.GET and request_param_name in request.GET:
                return request.GET.getlist(request_param_name)
            elif request.POST and request_param_name in request.POST:
                return request.POST.getlist(request_param_name)
            else:
                if raise_exception:
                    raise ValueError(f'Param {request_param_name} not found in request')
                else:
                    return default_value
    else:
        return None


def to_dict(obj, class_key=None):
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = to_dict(v, class_key)
        return data
    elif hasattr(obj, "_ast"):
        return to_dict(obj._ast())
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [to_dict(v, class_key) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, to_dict(value, class_key))
                     for key, value in obj.__dict__.items()
                     if not callable(value) and not key.startswith('_')])
        if class_key is not None and hasattr(obj, "__class__"):
            data[class_key] = obj.__class__.__name__
        return data
    else:
        return obj


def get_field_value(obj: any, field_name: str, default_val: any = None, can_call_function=True):
    if obj and field_name:
        if isinstance(obj, dict):
            return obj.get(field_name, default_val)
        elif isinstance(obj, collections.Sequence) and not isinstance(obj, str) and field_name.isnumeric():
            index = int(field_name)
            return default_val if len(obj) <= index else obj[index]
        elif hasattr(obj, field_name):
            val = getattr(obj, field_name)
            if can_call_function and callable(val):
                val = val()
            return val
        else:
            return default_val
    else:
        return None


def get_field_value_ex(obj: any, field_name: str, default_val: any = None, can_call_function=True):
    if obj is None:
        return default_val
    if '__' in field_name:
        fields = field_name.split('__')
        if fields:
            val = obj
            for field in fields:
                val = get_field_value(val, field, default_val)
                if val is None:
                    break
            return val
        return default_val
    else:
        return get_field_value(obj, field_name, default_val)


def my_serializer(obj, serialized_fields, deep_serialized_fields=True, exec_method=True, skip_none=False):
    result = {}
    current_obj = obj
    if serialized_fields and isinstance(current_obj, dict) or hasattr(current_obj, "__dict__"):
        for field_desc in serialized_fields:
            current_obj = obj
            field_name, convertor, result_field, default_dict, ignore_error = get_from_container(field_desc, [
                ('field_name', None),
                ('convertor', None),
                ('result_field', None),
                ('default_dict', False),
                ('ignore_error', True),
            ], True)

            if result_field is None:
                result_field = field_name

            current_val = get_field_value_ex(obj, field_name, None, exec_method)

            if current_val:
                result[result_field] = standard_value_converter(current_val, convertor, ignore_error, default_dict)
            else:
                if not skip_none:
                    result[result_field] = None
    else:
        result = to_dict(current_obj)
    return result


def standard_serializer(list_object):
    return serializers.serialize('json', list_object)


def dict_serializer(list_object):
    return [to_dict(obj) for obj in list_object]


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


def get_from_container(container, field_list_with_default_values: List[Tuple[str, any]], use_container_as_value=False,
                       ignore_iterable=False):
    result = []
    if isinstance(container, str) and use_container_as_value:
        result = [def_value for field_name, def_value in field_list_with_default_values]
        result[0] = container
    elif isinstance(container, Dict):
        for field_name, def_value in field_list_with_default_values:
            result.append(container.get(field_name, def_value))
    elif not ignore_iterable and isinstance(container, Iterable):
        result = [def_value for field_name, def_value in field_list_with_default_values]
        for index, value_for_field in enumerate(container[:len(result)]):
            result[index] = value_for_field
    elif use_container_as_value:
        result = [def_value for field_name, def_value in field_list_with_default_values]
        result[0] = container
    else:
        result = None
    return result


def standard_value_converter(value, converter, ignore_conversion_error=True,
                             default_convert_to_dict=True):
    if value is not None and converter:
        try:
            if callable(converter):
                converted_value = converter(value)
            elif isinstance(converter, str):
                if converter == 'int':
                    converted_value = int(value)
                elif converter == 'float':
                    converted_value = float(value)
                elif converter == 'dict':
                    converted_value = to_dict(value)
                elif converter.startswith() == 'serialize':
                    field_def = converter[9:-1].split(',')
                    if field_def:
                        converted_value = my_serializer(value, field_def)
                    else:
                        converted_value = to_dict(value)
                else:
                    converted_value = str(value)
        except ValueError as err:
            print('Convert value error')
            if not ignore_conversion_error:
                raise err
            else:
                print('Convert value error')
                return None
    else:
        if hasattr(value, 'serializer'):
            serializer = getattr(value, "serializer", None)
            if callable(serializer):
                return serializer(value)
            return None
        elif isinstance(value, (int, float, bool, str)) or not default_convert_to_dict:
            converted_value = str(value)
        elif default_convert_to_dict:
            converted_value = to_dict(value)
        else:
            converted_value = str(value)
    return converted_value


# Метод производит генерацию словаря для фильтрации из данных формы полученной GET или POST запросом
#  request - объект Request из запроса
# filter_list - описание полей в форме сиска содержащего строки с именами полей или словарь с полями
# dict(    'field_name' - имя поля
#          'field_action' - действие фильтрации icontains, equal, .... (не обязательное)
#          'form_field_name' - имя поля в форме (не обязательное)
#          'form_field_converter' - преобразователь занчений формы (конвенртор) (не обязательное)
#          'filter_as_value' - указывать разбирать значение формы как пару значение формы и действие
# )
# или tuple со значениями
# tuple(   имя поля,
#          действие фильтрации icontains, equal, ...., (не обязательное)
#          имя поля в форме, (не обязательное)
#          преобразователь занчений формы (конвенртор) (не обязательное)
# )
def form_filter_dict(request, filter_list, default_filter_action='icontains'):
    if filter_list:
        filter_dict = {}
        form_values = {}
        form_field_converter = None
        value_as_filter = True
        for filter_field_name in filter_list:
            current_field = None
            form_field_name = None
            filter_action = None
            if isinstance(filter_field_name, str):
                value = get_from_request(request, filter_field_name)
                current_field = filter_field_name
                filter_action = default_filter_action

            elif isinstance(filter_field_name, Dict) or isinstance(filter_field_name, Iterable):
                current_field, filter_action, form_field_name, form_field_converter, value_as_filter = get_from_container(
                    filter_field_name, [
                        ('field_name', None),
                        ('field_action', default_filter_action),
                        ('form_field_name', None),
                        ('form_field_converter', None),
                        ('value_as_filter', True),
                    ])
            if form_field_name is None:
                form_field_name = current_field

            value = get_from_request(request, form_field_name)
            if current_field and value:
                if not isinstance(value, str) and isinstance(value, Dict) or isinstance(value, Iterable):
                    current_value, filter_action = get_from_container(value, [
                        ('value', None),
                        ('action', filter_action)
                    ], True, ignore_iterable=not value_as_filter)
                else:
                    current_value = value
                current_value = standard_value_converter(current_value, form_field_converter)
                if current_value:
                    if filter_action:
                        filter_dict[f'{current_field}__{filter_action}'] = current_value
                    else:
                        filter_dict[f'{current_field}'] = current_value
                    form_values[form_field_name] = current_value

        return filter_dict, form_values
    else:
        return None, None


def create_thumbnail(original_file, thb_file_name, size=(100, 60)):
    image = Image.open(original_file)
    image.thumbnail(size)
    image.save(thb_file_name)


def get_image_data(dir, template, title='Car Photo ', thb_size=(150, 90), prepend_url=''):
    result = []
    filter = dir + '/' + template
    if os.path.exists(dir) and os.path.isdir(dir):
        count = 0
        for infile in glob.glob(filter):
            count += 1
            base_name = os.path.basename(infile)
            path = os.path.dirname(infile)
            thd_name = 'thb_' + base_name
            thd_file = os.path.join(path, thd_name)
            if not os.path.exists(thd_file):
                create_thumbnail(infile, thd_file, thb_size)

            result.append({
                'itemImageSrc': f'{prepend_url}/{base_name}' if prepend_url else base_name,
                'thumbnailImageSrc': f'{prepend_url}/{thd_name}' if prepend_url else thd_name,
                'title': f'{title} {count}'
            })
    return result
