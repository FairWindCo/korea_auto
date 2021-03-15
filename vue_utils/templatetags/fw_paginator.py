from typing import Iterable, Sized

from django import template
from django.utils.http import urlencode

register = template.Library()


def search(request_p, orders_, name, fieldname, params_dic):
    post_value = get_deep_values_of_object(request_p, 'POST', name, default=None)
    get_value = get_deep_values_of_object(request_p, 'GET', name, default=None)
    if post_value:
        params_dic[name] = post_value
        return orders_.filter(**{fieldname: post_value})
    elif get_value:
        params_dic[name] = get_value
        return orders_.filter(**{fieldname: get_value})
    else:
        return orders_


def create_page_range(current_page, max_pages, before_page=True, show_page_count=2):
    if before_page:
        if current_page - show_page_count <= 0:
            return range(1, current_page)
        else:
            return range(current_page - show_page_count, current_page)
    else:
        if current_page + show_page_count > max_pages:
            return range(current_page + 1, max_pages + 1)
        else:
            return range(current_page + 1, current_page + show_page_count)


@register.filter(name='paginator_before')
def paginator_before(current_page, max_pages, show_page_count=2):
    return create_page_range(current_page, max_pages, True, show_page_count)


@register.filter(name='paginator_after')
def paginator_before(current_page, max_pages, show_page_count=2):
    return create_page_range(current_page, max_pages, False, show_page_count)


@register.inclusion_tag('vue_utils/paginator.html', takes_context=True)
def paging_navigation(context, page, params=None, *args, **kwargs):
    max_page_btn = 10
    if 'max_page_btn' in kwargs:
        max_page_btn = kwargs['max_page_btn']
    rng = page.paginator.page_range
    return {
        'page_obj': page,
        'param': params,
        'max_page_btn': max_page_btn,
        'page_before_range': create_page_range(page.number, page.paginator.num_pages, True, max_page_btn),
        'page_after_range': create_page_range(page.number, page.paginator.num_pages, False, max_page_btn),
        'total_page_range': rng
    }


@register.simple_tag
def get_url_replace(request, field, value):
    d = request.GET.copy()
    d[field] = value
    return urlencode(d)


@register.simple_tag
def get_url_delete(request, field):
    d = request.GET.copy()
    del d[field]
    return urlencode(d)


def get_value_of_object(object, key, default=None):
    if object:
        if key in object:
            return object[key]
        elif hasattr(object, key):
            return getattr(object, key, default)
        else:
            return default
    else:
        return default


def get_deep_values_of_object(object, *key, default=None):
    value = default
    _current_obj = object
    if _current_obj:
        if key:
            for sub in key:
                if sub is None:
                    continue
                value = get_value_of_object(_current_obj, sub, default)
                if value:
                    _current_obj = value
                else:
                    return default
            return value
    else:
        return default


def combine_requests(context, use_post=True, clear_array=True):
    if 'fw_special_all_request' in context:
        # print('FROM CONTEXT', context['fw_special_all_request'])
        return context['fw_special_all_request']
    d = {}
    # request = get_value_of_object(context, 'request', None)
    # if request and request.GET:
    #     d.update(**request.GET)
    # if use_post and request and request.POST:
    #     d.update(**request.POST)
    get_request = get_deep_values_of_object(context, 'request', 'GET', default=None)
    if get_request:
        d.update(**get_request)
    post_request = get_deep_values_of_object(context, 'request', 'POST', default=None)
    if use_post and post_request:
        d.update(**post_request)
    if clear_array:
        for k, v in d.items():
            if isinstance(v, Sized)  and len(v) == 1:
                d[k] = v[0]
            elif isinstance(v, Iterable):
                d[k] = next(v.__iter__())
    context['fw_special_all_request'] = d
    return d


@register.simple_tag(takes_context=True)
def url_delete(context, field):
    request_params = combine_requests(context)
    if field in request_params:
        del request_params[field]
    return urlencode(request_params)


@register.simple_tag(takes_context=True)
def url_replace(context, field, value):
    request_params = combine_requests(context)
    if field in request_params:
        request_params[field] = value
    return urlencode(request_params)


@register.simple_tag(takes_context=True)
def param_replace(context, param, **kwargs):
    """
    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.
    It also removes any empty parameters to keep things neat,
    so you can remove a parm by setting it to ``""``.
    For example, if you're on the page ``/things/?with_frosting=true&page=5``,
    then
    <a href="/things/?{% param_replace page=3 %}">Page 3</a>
    would expand to
    <a href="/things/?with_frosting=true&page=3">Page 3</a>
    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    # print(context)
    if param is None:
        param = {}

    d = combine_requests(context, use_post=kwargs.get('use_post', True), clear_array=kwargs.get('clear_array', True))
    # print('INPUT CONTEXT', d)
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]

    for pk, pv in param.items():
        d[pk] = pv

    # print('OUTPUT CONTEXT', d)
    return urlencode(d)


@register.simple_tag(takes_context=True)
def form_url(context, param=None, **kwargs):
    request = get_value_of_object(context, 'request', None)
    url = request.build_absolute_uri('?') if request else ''
    url = f'{url}?{param_replace(context, param, **kwargs)}'
    # print('URL=', url)
    return url
