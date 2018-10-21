import unittest
from unittest import TestCase

from gp.brainfuck_machine import BrainfuckEmulator


class TestBFMRun(TestCase):
    """
    Test the function `gene.run(gene, input_stack)`
    """

    def setUp(self):
        """Define useful variables for tests"""
        self.hello_world = '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]' \
                           '>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.' \
                           '>>+.>++.'

    def test_empty_case(self):
        """Test the empty case"""
        self.assertEqual(BrainfuckEmulator('', '', 10).run(), '')

    def test_hello_world(self):
        """Test Wikipedia's `Hello world!` program"""
        self.assertEqual(BrainfuckEmulator(self.hello_world, '', 1000).run(),
                         'Hello World!\n')

    def test_input(self):
        """Test taking input"""
        self.assertEqual(BrainfuckEmulator(',+.', 'A', 10).run(), 'B')


class TestBFMLoopMap(TestCase):
    """Test the function `gene.loop_map(gene)`"""

    def setUp(self):
        """Define useful variables"""
        self.hello_world = '++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]' \
                           '>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.' \
                           '>>+.>++.'

    def test_base_case(self):
        self.assertEqual(BrainfuckEmulator._loop_map(''), {})

    def test_trivial_case(self):
        self.assertEqual(BrainfuckEmulator._loop_map('[]'), {0: 1, 1: 0})

    def test_hello_world(self):
        self.assertEqual(BrainfuckEmulator._loop_map(self.hello_world),
                         {48: 8, 33: 14, 8: 48, 43: 45, 45: 43, 14: 33})


if __name__ == '__main__':
    unittest.main()
