from django.shortcuts import render
# Create your views here.
from django.views.generic import ListView

from vue_utils.utils import form_filter_dict


def view_test(request):
    return render(request, 'vue_utils/vue_base_template.html', context={})


class FilterListView(ListView):
    """A base view for displaying a list of objects."""

    filters_fields = None
    last_request = None
    default_filter_action = 'icontains'
    additional_static_attribute = {}
    filter_form_values = {}

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
        return list_objects

    def get(self, request, *args, **kwargs):
        self.last_request = request
        return super(FilterListView, self).get(request, *args, *kwargs)

    def post(self, request, *args, **kwargs):
        self.last_request = request
        return super(FilterListView, self).get(request, *args, *kwargs)
