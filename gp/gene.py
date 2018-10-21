from __future__ import annotations

import logging
import random
from typing import Optional, Tuple, Union

from gp.brainfuck_machine import BrainfuckEmulator
from gp.trainer import Trainer


class Gene(object):
    """Representation of a `Gene` and all the relevant data surrounding it"""
    log = logging.getLogger(__name__)
    __output = None
    __fitness = None

    def __init__(self,
                 trainer: Trainer,
                 gene: str) -> None:
        """Load data we need"""
        self.__trainer = trainer
        self.gene = gene

    def __iter__(self):
        """Allow iterating through the gene string"""
        self.__index = 0
        return iter(self.gene)

    def __next__(self):
        """Get the next element of the containing string"""
        if self.__index <= len(self):
            return self.gene[self.__index]
        else:
            raise StopIteration

    def __getitem__(self, item):
        """Allow getting string slices of the gene together with __len__"""
        return self.gene[item]

    def __repr__(self):
        return '<Gene: Fitness={}, Code={}...>'.format(self.fitness(),
                                                       self.gene[:16])

    def __len__(self):
        """We store this function as a property, and cache the value of it"""
        return len(self.gene)

    def fitness(self) -> Union[int, float]:
        """The fitness of the particular gene as a property, cached"""
        if self.__fitness is None:
            self.__fitness = self.__trainer.check_fitness(self.output())
        return self.__fitness

    async def output(self, max_iter: int = 100_000) -> str:
        """
        The output of running the gene with a particular input

        :param max_iter: Maximum iterations the can program
        :return: What the program wrote to output
        """
        # cache results of emulator
        if self.__output is None:
            self.__output = BrainfuckEmulator(self.gene,
                                              self.__trainer.gen_in(),
                                              max_iter).run()
        return self.__output

    @staticmethod
    def gen(mu: Optional[float] = None,
            sigma: Optional[float] = None,
            length: Optional[int] = None) -> Union[Tuple[str, int], str]:
        """
        Generate a random Brainfuck program

        :param length:
        :param mu: Average program length
        :param sigma: Standard deviation of program length
        :return:  String containing a valid Brainfuck program
        """
        commands = (
            (2, '>'),
            (2, '<'),
            (2, '+'),
            (2, '-'),
            (2, '.'),
            (2, ','),
            (1, '['),
            (1, ']'),
        )
        if not length:
            length = int(random.gauss(mu, sigma))

        code = ''

        # make a program to length
        while length > 0:
            c = random.choice(commands)

            # recursively create balanced brackets
            if c[1] == '[':
                inner, length = Gene.__inner_gen(length - 1)
                code += '[{}]'.format(inner)
            elif c[1] == ']':
                length -= 1
            else:
                code += c[1]
                length -= 1
        else:
            return code

    @staticmethod
    def __inner_gen(length: int) -> Tuple[str, int]:
        commands = (
            (2, '>'),
            (2, '<'),
            (2, '+'),
            (2, '-'),
            (2, '.'),
            (2, ','),
            (1, '['),
            (1, ']'),
        )
        code = ''
        while length > 0:
            c = random.choice(commands)
            if c[1] == '[':
                inner, length = Gene.__inner_gen(length - 2)
                code += '[{}]'.format(inner)
            elif c[1] == ']':
                return code, length
            else:
                code += c[1]
                length -= 1
        else:
            return code, length

    @staticmethod
    def repair(code: str) -> str:
        """
        "Repairs" broken codes by balancing brackets

        :param code: String containing an invalid Brainfuck program
        :return:  String containing a valid Brainfuck program
        """
        stack_counter = 0
        s = ''

        for i in code:
            if i == '[':
                stack_counter += 1
                s += i
            elif i == ']':
                # handle too many right brackets
                if stack_counter:
                    s += i
                    stack_counter -= 1
            else:
                s += i
        # handle too many left brackets
        while stack_counter:
            s += ']'
            stack_counter -= 1
        return s
