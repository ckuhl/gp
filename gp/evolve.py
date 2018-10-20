import datetime
from typing import Any, List, Tuple

from termcolor import cprint

from . import gene, utils


class Evolve(object):
    """
    Class to evolve a genetic program
    """

    def __init__(self, prog_trainer, per_gen: int = 25):
        """Set up the Evolve-r with the program trainer and number of genes"""
        self.trainer = prog_trainer()
        self.per_gen = per_gen

    def generate_solution(self) -> str:
        """Create a genetic program that solves the defined problem"""
        gen_num = 0
        gen_results = self.generation_zero()
        start = datetime.datetime.now()
        prev_soln = ''
        while gen_results[0][0] != 0:
            gen_num += 1
            gen_next = self.offspring(gen_results)
            gen_results = self.generation_n(gen_next)

            if __debug__:
                # logging
                cprint('[Gen #' + str(gen_num) + ']', 'magenta', sep='',
                       end='\t')
                stop = datetime.datetime.now()
                cprint('[' + str(stop - start)[:7] + ']', 'blue', sep='',
                       end='\t')
                print('Best fitness:', gen_results[0][0], sep='', end='\t')
                print(utils.visualize_control_chars(
                    gene.Gene.run(gen_results[0][1], '')[:len('Hello world!')]))
                if gen_results[0][1] != prev_soln:
                    prev_soln = gen_results[0][1]
                    print(prev_soln)

        return gen_results[0][1]

    def generation_zero(self) -> List[Tuple[Any, str]]:
        """Generate the seed generation to iterate on"""
        program_generation = []
        gen_round = 0
        while len(program_generation) < self.per_gen:
            g = gene.Gene.gen(350, 75)
            g_out = gene.Gene.run(g, self.trainer.gen_in())
            fitness = self.trainer.check_fitness(g_out)

            gen_round += 1
            if fitness != float('inf'):
                if __debug__:
                    print('=' * 79)

                    # loop through code to print it nicely
                    tmp_g = g
                    while tmp_g:
                        print(tmp_g[:79])
                        tmp_g = tmp_g[79:]

                    cprint('[INFO]', 'green', sep='', end='\t')
                    print('Number:', len(program_generation) + 1,
                          'Round:', gen_round + 1,
                          sep='\t', end='\t')
                    print('Fit:', fitness, sep='\t', end='\n')
                    print(utils.visualize_control_chars(g_out[:79]))

                program_generation.append((fitness, g))

        program_generation.sort()
        return program_generation

    def generation_n(self, gene_list: List[str]) -> List[Tuple[Any, str]]:
        """
        Iterate over a set of generated programs for a fitness function.
        :return: A list of program-fitness tuples
        """
        next_gen = []

        for i in gene_list:
            g_out = gene.Gene.run(i, self.trainer.gen_in())
            fitness = self.trainer.check_fitness(g_out)
            next_gen.append((fitness, i))

        next_gen.sort()
        return next_gen

    def offspring(self, prog_gen: List[Tuple[Any, str]]) -> List[str]:
        """
        Generate offspring for a given generation / health

        :param prog_gen: Program generation tuples (score, gene)
        :return: List of new genes
        """
        next_gen = []
        next_gen += [prog_gen[0][1]]  # take best from last round
        while len(next_gen) < self.per_gen:
            w1 = utils.weighted_choice(prog_gen)[0]
            w2 = utils.weighted_choice(prog_gen)[0]

            # Shim while moving over to Gene objects
            next_gen += gene.Gene.mutate(gene.Gene(self.trainer, ''), w1, w2)
        return next_gen
