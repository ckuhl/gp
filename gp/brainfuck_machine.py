import logging
from functools import lru_cache
from typing import Dict


log = logging.getLogger(__name__)


class BrainfuckMachine:
    """Virtual machine that emulates a simple Brainfuck interpreter"""
    # set the program pointer and data pointer
    dptr, pptr = 0, 0

    # TODO: Consider replacing the data list with a dict
    # data tape, and call stack
    data, stack = [0], []

    # step of iteration
    step = 0

    # output string
    out = ''

    def __init__(self, code: str,
                 input_string: str,
                 max_iter: int) -> None:
        self.input_stack = input_string

        self.code = code
        self.code_len = len(code)
        self.jmp_map = self._loop_map(code)

        self.max_iter = max_iter

    @staticmethod
    def _loop_map(code: str) -> Dict[int, int]:
        """
        Build a map of matching brackets, forwards and backwards

        :param code: String containing a valid Brainfuck program
        :return: Dictionary containing location of every bracket's match
        """
        stack, bmap = [], {}
        for n, c in enumerate(code):
            if c == '[':
                stack.append(n)
            elif c == ']':
                bmap[n] = stack.pop()  # back ref i.e. pos(']'): pos('[')
                bmap[bmap[n]] = n  # forward ref i.e pos('['): pos(']')
        return bmap

    def __move_pointer_right(self):
        self.dptr += 1
        try:
            self.data[self.dptr]
        except IndexError:  # accessing beyond tape end; extend tape
            self.data.append(0)
        self.pptr += 1

    def __bf_command_move_pointer_left(self) -> None:
        try:
            # test if we are at the start of the list
            self.data[self.dptr - 1]
            self.dptr -= 1
        except IndexError:
            # if we are, extend the list instead of moving the pointer
            self.data.insert(0, 0)
        self.pptr += 1

    def __bf_command_increment_cell(self) -> None:
        self.data[self.dptr] += 1
        self.pptr += 1

    def __bf_command_decrement_cell(self) -> None:
        self.data[self.dptr] -= 1
        self.pptr += 1

    def __bf_command_produce_output(self) -> None:
        if self.data[self.dptr] >= 0:
            self.out += chr(self.data[self.dptr])
        self.pptr += 1

    def __bf_command_take_input(self) -> None:
        if self.input_stack:
            self.data[self.dptr] = ord(self.input_stack[0])
            self.input_stack = self.input_stack[1:]
        self.pptr += 1

    def __bf_command_begin_loop(self) -> None:
        if self.data[self.dptr]:
            self.pptr += 1
        else:
            self.pptr = self.jmp_map[self.pptr]

    def __bf_command_end_loop(self) -> None:
        if self.data[self.dptr]:
            self.pptr = self.jmp_map[self.pptr]
        else:
            self.pptr += 1

    @lru_cache(maxsize=1)
    def run(self) -> str:
        """
        This functions as a switch statement...
        A large amount of time was spent at each "elif" branch, so this
        _should_ be faster
        :return: the program output
        """
        while self.pptr < self.code_len:
            {
                '>': self.__move_pointer_right,
                '<': self.__bf_command_move_pointer_left,
                '+': self.__bf_command_increment_cell,
                '-': self.__bf_command_decrement_cell,
                ',': self.__bf_command_take_input,
                '.': self.__bf_command_produce_output,
                '[': self.__bf_command_begin_loop,
                ']': self.__bf_command_end_loop,
            }[self.code[self.pptr]]()

            self.step += 1

            if self.step > self.max_iter:
                log.info('Max iteration of %s cycles, returning early',
                         self.max_iter)
                return self.out

        log.info('Program completed in %s cycles', self.max_iter)
        return self.out
