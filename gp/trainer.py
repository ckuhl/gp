import logging
from typing import Union


log = logging.getLogger(__name__)


class Trainer:
    """
    A genetic program trainer provides a method by which to generate inputs,
      expected outputs, and a fitness calculator by which to train functions.
    """

    def __init__(self):
        """Configure the trainer"""
        pass

    def gen_in(self) -> str:
        """Generate input for a program"""
        raise NotImplementedError

    def gen_out(self) -> str:
        """Generate the expected output given the above input"""
        raise NotImplementedError

    def check_fitness(self, output: str) -> Union[int, float]:
        """
        Given an output, generate a number between [0, +inf) that indicates the
        fitness of a particular gene.
        """
        raise NotImplementedError


class Hello(Trainer):
    """A trainer to generate a program that what writes out `Hello World!`"""

    def __init__(self):
        """
        TODO: Does Hello need anything set up?
        """
        super().__init__()

    def gen_in(self):
        """
        TODO: Should any input be provided?
        """
        return ''

    def gen_out(self):
        return 'Hello world!'

    def check_fitness(self, output):
        """
        Calculate how close the output is to "Hello world!"

        The distance between strings is calculated is the square of the
        difference between each ASCII character.
        """
        expected = self.gen_out()
        fitness = 0
        for n, i in enumerate(expected):
            try:
                fitness += abs(ord(i) - ord(output[n])) ** 2
            except IndexError:
                return float('inf')
        log.info('Expected: %s\nGot: %s\nFitness: %s', expected, output,
                 fitness)
        return fitness
