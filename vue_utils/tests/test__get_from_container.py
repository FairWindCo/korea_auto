import unittest

from vue_utils.utils import get_from_container


class TestStringMethods(unittest.TestCase):

    def test_get_from_container_dict(self):
        test_dict = {
            'f1': 'test_value_1',
            'f2': 'test_value_2',
        }

        result = get_from_container(test_dict, [('f1', 'val1'), ('f2', 'val2'), ('f3', 'val1'), ('f4', 'val2')])
        self.assertEqual(['test_value_1', 'test_value_2', 'val1', 'val2'], result)

    def test_get_from_container_iter(self):
        test_dict = ['test_value_1', 'test_value_2']

        result = get_from_container(test_dict, [('f1', 'val1'), ('f2', 'val2'), ('f3', 'val1'), ('f4', 'val2')])
        self.assertEqual(['test_value_1', 'test_value_2', 'val1', 'val2'], result)

    def test_get_from_container_iter_shorter(self):
        test_dict = ['test_value_1', 'test_value_2']

        result = get_from_container(test_dict, [('f1', 'val1')])
        self.assertEqual(['test_value_1'], result)

    def test_get_from_container_iter_use_value(self):
        test_dict = 'test_value_1'

        result = get_from_container(test_dict, [('f1', 'val1'),  ('f3', 'val1')], True)
        self.assertEqual(['test_value_1', 'val1'], result)


if __name__ == '__main__':
    unittest.main()
