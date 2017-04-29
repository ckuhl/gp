from unittest import TestCase

from gp import gene


class TestGeneRun(TestCase):
    """
    Test the function `gene.run(gene, input_stack)`
    """
    def setUp(self):
        """Define useful variables for tests"""
        self.hello_world = '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'

    def test_empty_case(self):
        """Test the empty case"""
        self.assertEqual(gene.run('', ''), '')


    def test_hello_world(self):
        """Test Wikipedia's 'Hello world!' program"""
        self.assertEqual(gene.run(self.hello_world, ''), 'Hello World!\n')

    def test_input(self):
        """Test taking input"""
        self.assertEqual(gene.run(',+.', 'A'), 'B')


class TestGeneLoopMap(TestCase):
    """Test the function `gene.loop_map(gene)`"""
    def setUp(self):
        """Define useful variables"""
        self.hello_world = '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'

    def test_base_case(self):
        self.assertEqual(gene.loop_map(''), {})

    def test_trivial_case(self):
        self.assertEqual(gene.loop_map('[]'), {0: 1, 1: 0})

    def test_hello_world(self):
        self.assertEqual(gene.loop_map(self.hello_world), {48: 8, 33: 14, 8: 48, 43: 45, 45: 43, 14: 33})


class TestGeneValidate(TestCase):
    """
    Test the function `gene.validate(gene)`
    """
    def setUp(self):
        """Set up useful constants"""
        self.hello_world = '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'

    def test_empty_case(self):
        """Test for the empty case"""
        self.assertTrue(gene.validate(''))

    def test_hello_world(self):
        """Test Wikipedia's 'Hello world!' program"""
        self.assertTrue(gene.validate(self.hello_world))

    def test_unmatched_left_bracket(self):
        """Test for catching an unmatched left bracket"""
        self.assertFalse(gene.validate('[[[[][]]]'))

    def test_unmatched_right_bracket(self):
        """Test for catching an unmatched right bracket"""
        self.assertFalse(gene.validate('[[[][]]]]'))

    def test_matched_nested_brackets(self):
        """Test for properly parsing matching nested brackets"""
        self.assertTrue(gene.validate('[[[[[[[]]]]]]]'))


if __name__ == '__main__':
    unittest.main()
