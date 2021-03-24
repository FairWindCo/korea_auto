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

        result = form_filter_dict(test_request, ['field_1'])
        self.assertEqual({'field_1__icontains': 'car'}, result)

    def test_get_from_container_simple_with_additional(self):
        test_request = request_mok()
        test_request.GET = {
            'field_1': 'car',
            'field_2': 'blabla'
        }

        result = form_filter_dict(test_request, ['field_1'])
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

        result = form_filter_dict(test_request, ['field_1'])
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

        result = form_filter_dict(test_request, field_def)
        self.assertEqual({'car__equal': 'kia'}, result)

    def test_get_from_dict_value(self):
        test_request = request_mok()
        test_request.GET = {
            'field_1': {
                'value': 'car',
                'action': 'equal'
            }
        }

        result = form_filter_dict(test_request, ['field_1'])
        self.assertEqual({'field_1__equal': 'car'}, result)


if __name__ == '__main__':
    test = TestStringMethods.test_get_from_dict_value()
    unittest.main()
