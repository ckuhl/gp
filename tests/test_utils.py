from unittest import TestCase

from gp import utils


class TestVisualizeControlChars(TestCase):
    """
    Test the function `utils.visualize_control_chars(s)`
    """
    def setUp(self):
        """Define useful variables for tests"""
        self.chars = {'\a': '␇',
                      '\b': '␈',
                      '\f': '␌',
                      '\n': '␊',
                      '\r': '␍',
                      '\t': '␉',
                      '\v': '␋'}


    def test_empty_case(self):
        """Test the empty case"""
        self.assertEqual(utils.visualize_control_chars(''), '')


if __name__ == '__main__':
    unittest.main()

