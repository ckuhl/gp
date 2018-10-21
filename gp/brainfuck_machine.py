import collections
import logging
from typing import Dict


class MachineState(object):
    # set data pointer
    dptr = 50

    # set program pointer
    pptr = 0

    # initial data tape
    # TODO: Consider replacing the data list with a dict?
    data = [0] * 100


class BrainfuckEmulator(object):
    log = logging.getLogger(__name__)
    """Virtual machine that emulates a simple Brainfuck interpreter"""
    # store a list of states we've seen before
    # (if we see the exact same one twice, that means we're in an infinite loop)
    states = set()
    in_infinite_loop = False

    # step of iteration
    cycles = 0

    # output string
    out = ''

    def __init__(self, code: str,
                 input_string: str,
                 max_iter: int) -> None:
        self.state = MachineState()
        self.code: str = code
        self.code_len: int = len(code)
        self.jmp_map: Dict[int, int] = self._loop_map(code)

        self.input_stack: str = input_string

        self.max_iter: int = max_iter

    def _loop_map(self, code: str) -> Dict[int, int]:
        """
        Build a map of matching brackets, forwards and backwards

        :param code: A valid Brainfuck program
        :return: Location of every bracket's match
        """
        stack, bmap = collections.deque(), {}
        for n, c in enumerate(code):
            if c == '[':
                stack.append(n)
            elif c == ']':
                try:
                    bmap[n] = stack.pop()  # back ref i.e. pos(']'): pos('[')
                    bmap[bmap[n]] = n  # forward ref i.e pos('['): pos(']')
                except IndexError as e:
                    self.log.error(bmap)
                    self.log.error(code[:n + 1])
                    raise e

        return bmap

    def __bf_command_increment_dptr(self) -> None:
        self.state.dptr += 1
        try:
            __test = self.state.data[self.state.dptr]
        except IndexError:  # accessing beyond tape end; extend tape
            self.state.data.append(0)
        self.state.pptr += 1

    def __bf_command_decrement_dptr(self) -> None:
        if self.state.dptr:
            self.state.dptr -= 1
        else:
            self.state.data.insert(0, 0)
        self.state.pptr += 1

    def __bf_command_increment_cell(self) -> None:
        self.state.data[self.state.dptr] += 1
        self.state.pptr += 1

    def __bf_command_decrement_cell(self) -> None:
        self.state.data[self.state.dptr] -= 1
        self.state.pptr += 1

    def __bf_command_produce_output(self) -> None:
        if self.state.data[self.state.dptr] >= 0:
            self.out += chr(self.state.data[self.state.dptr])
        self.state.pptr += 1

    def __bf_command_take_input(self) -> None:
        if self.input_stack:
            self.state.data[self.state.dptr] = ord(self.input_stack[0])
            self.input_stack: str = self.input_stack[1:]
        self.state.pptr += 1

    def __bf_command_begin_loop(self) -> None:
        # Check that we've been here before
        current_state = hash(self.state)

        if current_state in self.states:
            self.in_infinite_loop = True
        else:
            self.states.add(current_state)

        # actual bracket logic
        if self.state.data[self.state.dptr]:
            self.state.pptr += 1
        else:
            self.state.pptr = self.jmp_map[self.state.pptr]

    def __bf_command_end_loop(self) -> None:
        if self.state.data[self.state.dptr]:
            self.state.pptr = self.jmp_map[self.state.pptr]
        else:
            self.state.pptr += 1

    def run(self) -> str:
        """
        This functions as a switch statement...
        A large amount of time was spent at each "elif" branch, so this
        _should_ be faster
        :return: the program output
        """
        while self.state.pptr < self.code_len:
            {
                '>': self.__bf_command_increment_dptr,
                '<': self.__bf_command_decrement_dptr,
                '+': self.__bf_command_increment_cell,
                '-': self.__bf_command_decrement_cell,
                ',': self.__bf_command_take_input,
                '.': self.__bf_command_produce_output,
                '[': self.__bf_command_begin_loop,
                ']': self.__bf_command_end_loop,
            }[self.code[self.state.pptr]]()
            self.cycles += 1

            if self.in_infinite_loop:
                # We return from here _a lot_, let's not log it
                return self.out

            if self.cycles > self.max_iter:
                self.log.debug('Max iteration of %s cycles, returning early',
                               self.max_iter)
                return self.out

        self.log.debug('Program completed in %s cycles', self.cycles)
        return self.out
