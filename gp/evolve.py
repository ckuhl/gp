# builtins
import datetime
import random

# third party
from termcolor import cprint

# module code
import gp.gene as gene  # brainfuck / "gene" simulation program
import gp.utils as utils


class Evolve(object):
    """
    Class to evolve a genetic program
    """
    def __init__(self, prog_trainer, per_gen=25):
        """
        Set up the Evolve-r with the program trainer and number of genes
        """
        self.trainer = prog_trainer()
        self.per_gen = per_gen

    def generate_solution(self):
        """
        Create a genetic program that solves the defined problem
        """
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
                cprint('[Gen #' + str(gen_num) + ']', 'magenta', sep='', end='\t')
                stop = datetime.datetime.now()
                cprint('[' + str(stop - start)[:7] + ']', 'blue', sep='', end='\t')
                print('Best fitness:', gen_results[0][0], sep='', end='\t')
                print(utils.visualize_control_chars(gene.run(gen_results[0][1], '')[:len('Hello world!')]))
                if gen_results[0][1] != prev_soln:
                    prev_soln = gen_results[0][1]
                    print(prev_soln)

        return gen_results[0][1]

    def generation_zero(self):
        """
        Generate the seed generation to iterate on
        """
        prog_gen = []
        gen_round = 0
        while len(prog_gen) < self.per_gen:
            g = gene.gen((random.randint(51, 500), random.randint(501, 1000)))
            g_out = gene.run(g, self.trainer.gen_in())
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
                    print('Number:', len(prog_gen) + 1, 'Round:', gen_round + 1, sep='\t', end='\t')
                    print('Fit:', fitness, sep='\t', end='\n')
                    print(utils.visualize_control_chars(g_out[:79]))

                prog_gen.append( (fitness, g) )

        prog_gen.sort()
        return prog_gen

    def generation_n(self, gene_list):
        """
        Iterate over a set of generated programs for a fitness function.
        :return: A list of program-fitness tuples
        """
        next_gen = []

        for i in gene_list:
            g_out = gene.run(i, self.trainer.gen_in())
            fitness = self.trainer.check_fitness(g_out)
            next_gen.append( (fitness, i) )

        next_gen.sort()
        return next_gen

    def offspring(self, prog_gen):
        """
        Generate offspring for a given generation / health
        """
        next_gen = []
        next_gen += [prog_gen[0][1]]  # take best from last round
        while len(next_gen) < self.per_gen:
            w1 = utils.weighted_choice(prog_gen)
            w2 = utils.weighted_choice(prog_gen)
            nw1, nw2 = self.crossover(w1, w2)
            next_gen += gene.mutate(nw1, nw2)
        return next_gen

    def crossover(self, prog1, prog2):
        """
        Cross over two genes
        """
        valid = False
        new1 = ''
        new2 = ''
        while not valid:
            cut1 = random.randint(0, len(prog1))
            cut2 = random.randint(0, len(prog2))
            new1 = prog1[cut1:] + prog2[:cut2]
            new2 = prog2[cut2:] + prog1[:cut1]
            # if the genes aren't valid, retry
            if not gene.validate(new1) and not gene.validate(new2):
                continue

            g1_out = gene.run(new1, self.trainer.gen_in())
            fitness1 = self.trainer.check_fitness(g1_out)
            g2_out = gene.run(new2, self.trainer.gen_in())
            fitness2 = self.trainer.check_fitness(g2_out)

            if fitness1 != float('inf') and fitness2 != float('inf'):
                valid = True
            else:
                continue

        return [new1, new2]
