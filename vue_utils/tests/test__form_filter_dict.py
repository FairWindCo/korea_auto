import unittest

from vue_utils.utils import form_filter_dict


class request_mok:
    GET = None
    POST = None


class TestStringMethods(unittest.TestCase):

    def test_get_from_container_simple(self):
        test_request = request_mok()
        test_request.GET = {
            'field_1': 'car'
        }

        result, form = form_filter_dict(test_request, ['field_1'])
        self.assertEqual({'field_1__icontains': 'car'}, result)

    def test_get_from_container_simple_with_additional(self):
        test_request = request_mok()
        test_request.GET = {
            'field_1': 'car',
            'field_2': 'blabla'
        }

        result, form = form_filter_dict(test_request, ['field_1'])
        self.assertEqual({'field_1__icontains': 'car'}, result)

    def test_get_from_container_simple_with_post(self):
        test_request = request_mok()
        test_request.GET = {
            'field_1': 'car',
            'field_2': 'blabla'
        }
        test_request.POST = {
            'field_1': 'super',
            'field_2': 'blabla'
        }

        result, form = form_filter_dict(test_request, ['field_1'])
        self.assertEqual({'field_1__icontains': 'car'}, result)

    def test_get_from_dict(self):
        test_request = request_mok()
        test_request.GET = {
            'field_1': 'kia',
            'field_2': 'blabla'
        }

        field_def = [
            {
                'field_name': 'car',
                'field_action': 'equal',
                'form_field_name': 'field_1',
            }
        ]

        result, form = form_filter_dict(test_request, field_def)
        self.assertEqual({'car__equal': 'kia'}, result)

    def test_get_from_dict_value(self):
        test_request = request_mok()
        test_request.GET = {
            'field_1': {
                'value': 'car',
                'action': 'equal'
            }
        }

        result, form = form_filter_dict(test_request, ['field_1'])
        self.assertEqual({'field_1__equal': 'car'}, result)

    def test_get_from_dict_value_form(self):
        test_request = request_mok()
        test_request.GET = {
            'field_1': {
                'value': 'car',
                'action': 'equal'
            }
        }

        result, form = form_filter_dict(test_request, ['field_1'])
        self.assertEqual({'field_1': 'car'}, form)

    def test_get_from_dict_with_convert(self):
        test_request = request_mok()
        test_request.GET = {
            'field_1': {
                'value': '10',
                'action': 'equal'
            }
        }
        field_def = [
            {
                'field_name': 'car',
                'field_action': 'equal',
                'form_field_name': 'field_1',
                'form_field_converter': 'int'
            }
        ]

        result, form = form_filter_dict(test_request, field_def)
        self.assertEqual({'car__equal': 10}, result)
        self.assertEqual({'field_1': 10}, form)

    def test_get_from_dict_with_convert_ignore_error(self):
        test_request = request_mok()
        test_request.GET = {
            'field_1': {
                'value': '10',
                'action': 'equal'
            }
        }
        field_def = [
            {
                'field_name': 'car',
                'field_action': 'equal',
                'form_field_name': 'field_1',
                'form_field_converter': 'int'
            }
        ]

        result, form = form_filter_dict(test_request, field_def)
        self.assertEqual({'car__equal': 10}, result)
        self.assertEqual({'field_1': 10}, form)

    def test_get_from_dict_with_custom_convert(self):
        test_request = request_mok()
        test_request.GET = {
            'field_1': {
                'value': '10',
                'action': 'equal'
            }
        }
        field_def = [
            {
                'field_name': 'car',
                'field_action': 'equal',
                'form_field_name': 'field_1',
                'form_field_converter': lambda v: int(v)
            }
        ]

        result, form = form_filter_dict(test_request, field_def)
        self.assertEqual({'car__equal': 10}, result)
        self.assertEqual({'field_1': 10}, form)


if __name__ == '__main__':
    unittest.main()
