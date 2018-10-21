import datetime
import logging
import random
from typing import List, Tuple

import termcolor

from gp.trainer import Trainer
from . import gene, utils
from .gene import Gene


class Evolve(object):
    log = logging.getLogger(__name__)

    def __init__(self, trainer: Trainer, genes_per_gen: int = 24) -> None:
        """
        Set up the Evolve-r with the program trainer and number of genes per
        generation
        """
        self.trainer = trainer
        self.per_gen = genes_per_gen

    def generate_solution(self) -> str:
        """Create a genetic program that solves the defined problem"""
        generation_counter = 0
        start = datetime.datetime.now()

        current_generation = self.generation_zero()
        while current_generation[0].fitness != 0:
            current_generation = self.offspring(current_generation)

            generation_counter += 1
            self.log.debug(
                termcolor.colored('[Gen #{}]\t'.format(generation_counter),
                                  color='magenta'))
            stop = datetime.datetime.now()
            self.log.debug(
                termcolor.colored('[{}]\t'.format(str(stop - start)[:7]),
                                  color='blue'))

        return current_generation[0].gene

    def generation_zero(self) -> List[Gene]:
        """Generate the seed generation to iterate on"""
        program_generation = []
        gen_round = 0
        while len(program_generation) < self.per_gen:
            g = gene.Gene(self.trainer, gene.Gene.gen(350, 75))
            fitness = g.fitness

            gen_round += 1

            if fitness != float('inf'):
                # debugging information
                self.log.debug('=' * 79)

                # loop through code to print it nicely
                tmp_g = g.gene
                while tmp_g:
                    self.log.debug(tmp_g[:79])
                    tmp_g = tmp_g[79:]

                self.log.debug(
                    termcolor.colored(
                        'Number:\t{}\t'
                        'Round:\t{}\t'
                        'Fit:\t{}\n'.format(
                            len(program_generation) + 1,
                            gen_round + 1,
                            fitness),
                        color='green'))
                self.log.debug(utils.visualize_control_chars(g[:79]))

                program_generation.append(g)

        program_generation.sort(key=lambda x: x.fitness)
        return program_generation

    def offspring(self,
                  generation: List[Gene],
                  survivors: int = 2) -> List[Gene]:
        """
        Generate offspring for a given generation / health

        :param generation: Program generation tuples (score, gene)
        :param survivors: Number of Genes to take into the next round
        :return: Next generation
        """
        generation.sort(key=lambda x: x.fitness)
        next_gen = generation[:survivors]  # take best from last generation

        while len(next_gen) < self.per_gen:
            w1 = utils.weighted_choice(generation, lambda x: x.fitness)
            w2 = utils.weighted_choice(generation, lambda x: x.fitness)

            n1, n2 = self.mutate(w1, w2)
            if n1.fitness < float('inf'):
                next_gen.append(n1)
            if n2.fitness < float('inf'):
                next_gen.append(n2)

        next_gen.sort(key=lambda x: x.fitness)
        print([x.fitness for x in next_gen])

        # Logging
        self.log.debug('Best fitness: %s\t', next_gen[0].fitness)
        self.log.debug(utils.visualize_control_chars(
            next_gen[0].output[:len('Hello world!')]))

        if next_gen[0].gene != generation[0].gene:
            previous_solution = generation[0].gene
            self.log.debug(previous_solution)

        return next_gen

    def mutate(self,
               g1: Gene,
               g2: Gene,
               mutation_odds: float = 0.03) -> Tuple[Gene, Gene]:
        """
        Mutate a given Brainfuck program in various ways
        :param g1: the subject program to mutate
        :param g2: the donor program to mutate
        :param mutation_odds: probability of a mutation happening
        :return: Two mutated Brainfuck programs
        """

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
            c = 0
            while True:
                c += 1
                average_mutation = mutation_odds * len(code)
                X = random.gauss(average_mutation, average_mutation / 3)
                x = int(abs(X))
                pos = random.randint(0, len(code))

                deleted = Gene.repair(code[:pos] + code[pos + x:])

                g = Gene(self.trainer, deleted)

                if g.fitness != float('inf'):
                    break

            self.log.warning('Deletion took %s attempts', c)
            return g

        def duplication(code: Gene) -> Gene:
            """
            Duplicate a section of the program

            :param code: Code to duplicate a segment of
            :return: Mutated code
            """
            c = 0
            while True:
                c += 1
                average_mutation = mutation_odds * len(code)
                X = random.gauss(average_mutation, average_mutation * 2)
                x = int(abs(X))
                pos = random.randint(0, len(code))

                if pos + x > len(code):
                    continue

                duplicated = Gene.repair(code[:pos + x]
                                         + code[pos:pos + x]
                                         + code[pos + x:])

                new_code = Gene(self.trainer, duplicated)

                if new_code.fitness != float('inf'):
                    break
            self.log.warning('Deletion took %s attempts', c)

            return new_code

        def inversion(code: Gene) -> Gene:
            """
            Invert a section of the program
            For example, abcdef -> aDCBef

            :param code: Code to invert a portion of
            :return: Mutated code
            """
            point = random.randint(0, len(code))
            size = random.randint(0, len(code)) // 10

            start = point
            stop = point

            s = code.gene

            # This should probably avoid unbalanced brackets. I think.
            while size > 0 and stop < len(s) and start >= 0:
                if s[stop] in {'[', ']'}:
                    if s[start] in {'[', ']'}:
                        start -= 1
                        stop += 1
                        size -= 2
                    else:
                        start -= 1
                        size -= 1
                else:
                    stop += 1
                    size -= 1

            segment = s[start:stop][::-1]
            return Gene(self.trainer, s[:start] + segment[::-1] + s[stop:])

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
            c = 0
            while True:
                c += 1
                cut1 = random.randint(0, len(code1))
                cut2 = random.randint(0, len(code2))

                tmp = 0  # try finding nearby brackets to speed up code
                d_needed = __depth(code2[cut2:])
                while __depth(code1[cut1:]) != d_needed and tmp < 10:
                    cut1 += 1
                    tmp += 1

                g1_out = Gene(self.trainer,
                              Gene.repair(code1[cut1:] + code2[:cut2]))
                g2_out = Gene(self.trainer,
                              Gene.repair(code2[cut2:] + code1[:cut1]))

                if g1_out.fitness != float('inf') and \
                        g2_out.fitness != float('inf'):
                    break

            self.log.warning('Deletion took %s attempts', c)

            return g1_out, g2_out

        # Commented out for now as the above is really nonoptimal...
        # TODO: Call the above mutations in varying amounts
        # if random.getrandbits(1):
        #     return translocation(g1, g2)
        # else:
        #     return deletion(g1), duplication(g2)
        return inversion(g1), inversion(g2)
