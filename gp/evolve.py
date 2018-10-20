import datetime
from typing import List

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

    def generation_zero(self) -> List[gene.Gene]:
        """Generate the seed generation to iterate on"""
        program_generation = []
        gen_round = 0
        while len(program_generation) < self.per_gen:
            g = gene.Gene(self.trainer, gene.Gene.gen(350, 75))
            fitness = g.fitness

            gen_round += 1
            if fitness != float('inf'):
                if __debug__:
                    print('=' * 79)

                    # loop through code to print it nicely
                    tmp_g = g.gene
                    while tmp_g:
                        print(tmp_g[:79])
                        tmp_g = tmp_g[79:]

                    cprint('[INFO]', 'green', sep='', end='\t')
                    print('Number:', len(program_generation) + 1,
                          'Round:', gen_round + 1,
                          sep='\t', end='\t')
                    print('Fit:', fitness, sep='\t', end='\n')
                    print(utils.visualize_control_chars(g[:79]))

                program_generation.append(g)

        program_generation.sort(key=lambda x: x.fitness)
        return program_generation

    def generation_n(self, gene_list: List[gene.Gene]) -> List[gene.Gene]:
        """
        Iterate over a set of generated programs for a fitness function.
        :return: A list of program-fitness tuples
        """
        gene_list.sort(key=lambda x: x.fitness)
        return gene_list

    def offspring(self, prog_gen: List[gene.Gene]) -> List[gene.Gene]:
        """
        Generate offspring for a given generation / health

        :param prog_gen: Program generation tuples (score, gene)
        :return: List of new genes
        """
        next_gen = []
        next_gen += [prog_gen[0]]  # take best from last round
        while len(next_gen) < self.per_gen:
            w1 = utils.weighted_choice(prog_gen, lambda x: x.fitness)
            w2 = utils.weighted_choice(prog_gen, lambda x: x.fitness)

            # Shim while moving over to Gene objects
            next_gen += gene.Gene.mutate(gene.Gene(self.trainer, ''), w1, w2)
        return next_gen
