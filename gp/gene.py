from __future__ import annotations

import logging
import random
from functools import lru_cache
from typing import Tuple, Union

from gp.brainfuck_machine import BrainfuckMachine
from gp.trainer import Trainer
from . import utils


log = logging.getLogger(__name__)


class Gene(object):
    """Representation of a `Gene` and all the relevant data surrounding it"""

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

    @lru_cache(maxsize=1)
    def __len__(self):
        """We store this function as a property, and cache the value of it"""
        return len(self.gene)

    @property
    @lru_cache(maxsize=1)
    def fitness(self) -> Union[int, float]:
        """The fitness of the particular gene as a property, cached"""
        return self.__trainer.check_fitness(self.output)

    @property
    @lru_cache(maxsize=10)
    def output(self, max_iter: int = 100_000) -> str:
        """
        The output of running the gene with a particular input

        :param max_iter: Maximum iterations the can program
        :return: What the program wrote to output
        """
        return BrainfuckMachine(self.gene,
                                self.__trainer.gen_in(),
                                max_iter).run()

    @staticmethod
    def gen(mu: float, sigma: float) -> str:
        """
        Generate a random Brainfuck program

        :param mu: Average program length
        :param sigma: Standard deviation of program length
        :return:  String containing a valid Brainfuck program
        """
        commands = [
            [1, '>', 0],
            [1, '<', 0],
            [1, '+', 0],
            [1, '-', 0],
            [1, '.', 0],
            [1, ',', 0],
            [1, '[', 1],
            [0, ']', -1],
        ]

        length = int(random.gauss(mu, sigma))
        code = ''
        depth = 0

        # make a program to length
        while length > 0:
            c = utils.weighted_choice(commands, key=lambda x: x[0])
            code += c[1]
            depth += c[2]
            commands[7][0] = depth  # make it more likely to close the bracket
            length -= 1

        # pad out with brackets
        while depth > 0:
            code += ']'
            depth -= 1

        return code

    @staticmethod
    def repair(code: str) -> str:
        """
        "Repairs" broken codes by balancing brackets

        :param code: String containing an invalid Brainfuck program
        :return:  String containing a valid Brainfuck program
        """
        stack = []
        s = ''

        for i in code:
            if i == '[':
                stack.append(']')
                s += i
            elif i == ']':
                # handle too many right brackets
                try:
                    s += stack.pop()
                except IndexError:
                    pass
            else:
                s += i
        # handle too many left brackets
        for i in stack:
            s += i
        return s

    def mutate(self,
               g1: Gene,
               g2: Gene) -> Tuple[Gene, Gene]:
        """
        Mutate a given Brainfuck program in various ways
        :param g1: the subject program to mutate
        :param g2: the donor program to mutate
        :return: Two mutated Brainfuck programs
        """
        MUTATION_ODDS = 0.03

        def __depth(code: str) -> int:
            """
            Depth (in number of `[` minus number of `]`) of code
            :param code: String, code fragment to determine depth of
            :return: Depth of brackets
            """
            d = 0
            for i in code:
                if i == '[':
                    d += 1
                elif i == ']':
                    d -= 1
            return d

        def deletion(code: Gene) -> Gene:
            """
            Delete a section of the program

            :param code: Code to delete a segment of
            :return: Mutated code
            """
            while True:
                average_mutation = MUTATION_ODDS * len(code)
                X = random.gauss(average_mutation, average_mutation / 3)
                x = int(abs(X))
                pos = random.randint(0, len(code))

                deleted = Gene.repair(code[:pos] + code[pos + x:])

                g = Gene(self.__trainer, deleted)

                if g.fitness != float('inf'):
                    break

            return g

        def duplication(code: Gene) -> Gene:
            """
            Duplicate a section of the program

            :param code: Code to duplicate a segment of
            :return: Mutated code
            """
            while True:
                average_mutation = MUTATION_ODDS * len(code)
                X = random.gauss(average_mutation, average_mutation * 2)
                x = int(abs(X))
                pos = random.randint(0, len(code))

                if pos + x > len(code):
                    continue

                duplicated = Gene.repair(code[:pos + x]
                                         + code[pos:pos + x]
                                         + code[pos + x:])

                new_code = Gene(self.__trainer, duplicated)

                if new_code.fitness != float('inf'):
                    break

            return new_code

        def inversion(code: Gene) -> Gene:
            """
            Invert a section of the program
            For example, abcdef -> aDCBef

            :param code: Code to invert a portion of
            :return: Mutated code
            """
            raise NotImplementedError

        def complementation(code: Gene) -> Gene:
            """
            Swap out code for it's complement
            Ex. +/-, [/], >/<, ,/.

            :param code: Code to complement a portion of
            :return: Mutated code
            """
            raise NotImplementedError

        def insertion(code1: Gene, code2: Gene) -> Tuple[Gene, Gene]:
            """
            Delete a section of program one and insert it into program two
            :param code1: "Donor" segment of code
            :param code2: "Receiver" segment of code
            :return: Mutated donor and receiver code
            """
            raise NotImplementedError

        def translocation(code1: Gene, code2: Gene) -> Tuple[Gene, Gene]:
            """
            Swap segments of code1 with code2

            :param code1: First segment of code
            :param code2: Second segment of code
            :return: Both mutated segments of code
            """
            while True:
                cut1 = random.randint(0, len(code1))
                cut2 = random.randint(0, len(code2))

                tmp = 0  # try finding nearby brackets to speed up code
                d_needed = __depth(code2[cut2:])
                while __depth(code1[cut1:]) != d_needed and tmp < 10:
                    cut1 += 1
                    tmp += 1

                g1_out = Gene(self.__trainer,
                              Gene.repair(code1[cut1:] + code2[:cut2]))
                g2_out = Gene(self.__trainer,
                              Gene.repair(code2[cut2:] + code1[:cut1]))

                if g1_out.fitness != float('inf') and \
                        g2_out.fitness != float('inf'):
                    break

            return g1_out, g2_out

        # TODO: Call the above mutations in varying amounts
        if random.getrandbits(1):
            return translocation(g1, g2)
        else:
            return deletion(g1), duplication(g2)
