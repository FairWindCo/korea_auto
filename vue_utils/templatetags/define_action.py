from django import template

register = template.Library()


@register.filter(name='times')
def times(number):
    return range(number)


def create_page_range(current_page, max_pages, before_page=True, show_page_count=2):
    if before_page:
        if current_page - show_page_count < 0:
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


@register.simple_tag
def define(val=None):
    return val


@register.simple_tag
def create_list(val=None, default_value=None, *args, **kwargs):
    if val is None or val == '':
        val = default_value.split(',')
    elif isinstance(val, str):
        val = val.split(',')
    print(val)
    return val


@register.filter
def create_default_list(val, default_value):
    if val is None or val == '':
        val = default_value.split(',')
    elif isinstance(val, str):
        val = val.split(',')
    print(val)
    return val
