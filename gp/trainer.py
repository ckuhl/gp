import gp.quadratic as quadratic  # quadratic equation functions
from termcolor import cprint


class Trainer(object):
    """
    A genetic program trainer provides a method by which to generate inputs,
      expected outputs, and a fitness calculator by which to train functions.
    """
    def __init__(self):
        """
        TODO
        """
        pass

    def gen_in(self):
        """
        TODO
        """
        pass

    def gen_out(self):
        """
        TODO
        """
        pass

    def check_fitness(self, output):
        """
        TODO
        """
        pass


class Quadratic(Trainer):
    """
    A trainer to generate programs that factor a quadratic equation into it's
      roots
    """
    def __init__(self):
        self.root_set = quadratic.gen_root_set(-10, 10)
        self.std_form = quadratic.gen_std_form(self.root_set)
        self.f = quadratic.gen_quadratic_eqn(self.root_set)

    def gen_in(self):
        """
        Generate a representation of a quadratic as 3 numbers "x y z"
        """
        return str(self.std_form[0]) + ' ' + str(self.std_form[1]) + ' ' + str(self.std_form[2])

    def check_fitness(self, output):
        """
        Return the average of the two points' distance from the roots (i.e. 0)
        """
        try:
            output_list = output.split()
            p1, p2 = float(output_list[0]), float(output_list[1])
        except ValueError:
            if __debug__:
                cprint('[ERROR]', 'red', sep='', end='\t')
                print('ValueError on program output')
            return float('inf')
        except IndexError:
            if __debug__:
                cprint('[ERROR]', 'red', sep='', end='\t')
                print('IndexError grabbing 2 values from program output')
            try:
                p1 = float(output_list[0])
                return abs(self.f(p1) * 0.5)
            except IndexError:
                if __debug__:
                    cprint('[ERROR]', 'red', sep='', end='\t')
                    print('IndexError grabbing 1 value from program output')
                return float('inf')

        avg_dist = (self.f(p1) + self.f(p2)) / 2

        # TODO: Normalize quadratic equation (eventually)
        return abs(avg_dist)

class Hello(Trainer):
    """
    A trainer to generate a program that outputs the string "Hello World!"
    """
    def __init__(self):
        """
        TODO
        """
        pass

    def gen_in(self):
        """
        TODO
        """
        return ''

    def check_fitness(self, output):
        """
        Calculate how close the output is to "Hello world!"

        The distance between strings is calculated is the square of the
        difference between each ASCII character.
        """
        hello_string = "Hello world!"
        fitness = 0
        for n, i in enumerate(hello_string):
            try:
                fitness += abs(ord(i) - ord(output[n])) ** 2
            except IndexError:
                #if __debug__:
                #    cprint('[ERROR]', 'red', sep='', end='\t')
                #    print('IndexError iterating through output')
                return float('inf')
        return fitness

