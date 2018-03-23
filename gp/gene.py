import random
import time

from termcolor import cprint

import utils


def run(code, input_stack, max_iter=100000):
    """
    Run a brainfuck program with a given input "stack" (i.e. string)

    :param code: String containing a valid Brainfuck program
    :param input_stack: String to feed into the program char by char
    :param max_iter: Maximum number of iterations to run the program
    :return: String containing program output
    """
    dptr, pptr = 0, 0  # set the program pointer and ata pointer
    data, stack = [0], []  # data tape, and call stack
    out = ''  # output string
    step = 0  # step of iteration
    jmp_map = loop_map(code)
    code_len = len(code)

    while pptr < code_len:
        if code[pptr] == '>':
            dptr += 1
            try:
                data[dptr]
            except IndexError:  # accessing beyond tape end; extend tape
                data.append(0)
            pptr += 1

        elif code[pptr] == '<':
            try:
                data[dptr - 1]
                dptr -= 1
            except IndexError:
                data.insert(0, 0)
            pptr += 1

        elif code[pptr] == '+':
            data[dptr] += 1
            pptr += 1

        elif code[pptr] == '-':
            data[dptr] -= 1
            pptr += 1

        elif code[pptr] == '.':
            if data[dptr] >= 0:
                out += chr(data[dptr])
            pptr += 1

        elif code[pptr] == ',':
            if input_stack:
                data[dptr] = ord(input_stack[0])
                input_stack = input_stack[1:]
            pptr += 1

        elif code[pptr] == '[':
            if data[dptr]:
                pptr += 1
            else:
                pptr = jmp_map[pptr]

        elif code[pptr] == ']':
            if data[dptr]:
                pptr = jmp_map[pptr]
            else:
                pptr += 1
        step += 1
        if step > max_iter:
            return out
    return out


def loop_map(code):
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


def gen(mu, sigma):
    """
    Generate a random Brainfuck program

    :param mu: Average program length
    :param sigma: Std. dev. of program length
    :return:  String containing a valid Brainfuck program
    """
    valid = False
    cmds = [[1, '>', 0], [1, '<', 0],
            [1, '+', 0], [1, '-', 0],
            [1, '.', 0], [1, ',', 0],
            [1, '[', 1], [0, ']', -1]]

    length = int(random.gauss(mu, sigma))
    code = ''
    depth = 0

    # make a program to length
    while length > 0:
        c = utils.weighted_choice(cmds)
        code += c[0]
        depth += c[1]
        cmds[7][0] = depth  # make it more likely to close the bracket
        length -= 1

    # pad out with brackets
    while depth > 0:
        code += ']'
        depth -= 1

    return code


def repair(code):
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


def mutate(trainer, code1, code2):
    """
    Mutate a given Brainfuck program in various ways
    :param code1: String, the subject program to mutate
    :param code2: String, the donor program to mutate
    :return: String, a mutated brainfuck program
    """
    MUTATION_ODDS = 0.03

    def depth(code):
        """
        Depth (in number of `[` minus number of `]`) of code
        :param code: String, code fragment to determine depth of
        :return: Integer
        """
        d = 0
        for i in code:
            if i == '[':
                d += 1
            elif i == ']':
                d -= 1
        return d


    def deletion(code):
        """
        Delete a section of the program

        :param code: Code to delete a segment of
        :return: Mutated code
        """
        valid = False
        new_code = ''

        while not valid:
            average_mutation = MUTATION_ODDS * len(code)
            X = random.gauss(average_mutation, average_mutation / 3)
            x = int(abs(X))
            pos = random.randint(0, len(code))

            new_code = repair(code[:pos] + code[pos + x:])

            g = run(new_code, trainer.gen_in())
            fitness = trainer.check_fitness(g)

            if fitness != float('inf'):
                valid = True
            else:
                continue

        return new_code


    def duplication(code):
        """
        Duplicate a section of the program

        :param code: Code to duplicate a segment of
        :return: Mutated code
        """
        valid = False
        new_code = ''
        while not valid:
            average_mutation = MUTATION_ODDS * len(code)
            X = random.gauss(average_mutation, average_mutation  * 2)
            x = int(abs(X))
            pos = random.randint(0, len(code))

            if pos + x  > len(code):
                continue

            new_code = repair(code[:pos + x] + code[pos:pos + x] + code[pos + x:])

            g = run(new_code, trainer.gen_in())
            fitness = trainer.check_fitness(g)

            if fitness != float('inf'):
                valid = True
            else:
                continue

        return new_code


    def inversion(code):
        """
        Invert a section of the program
        For example, abcdef -> aDCBef

        :param code: Code to invert a portion of
        :return: Mutated code
        """
        # TODO
        return code

    def complementation(code):
        """
        Swap out code for it's complement
        Ex. +/-, [/], >/<, ,/.

        :param code: Code to complement a portion of
        :return: Mutated code
        """
        # TODO
        return code

    def insertion(code1, code2):
        """
        Delete a section of program one and insert it into program two
        :param code1: "Donor" segment of code
        :param code2: "Receiver" segment of code
        :return: Mutated donor and receiver code
        """
        # TODO
        return code1, code2

    def translocation(code1, code2):
        """
        Swap segments of code1 with code2

        :param code1: First segment of code
        :param code2: Second segment of code
        :return: Both mutated segments of code
        """
        valid = False
        new1 = ''
        new2 = ''
        while not valid:
            cut1 = random.randint(0, len(code1))
            cut2 = random.randint(0, len(code2))

            tmp = 0  # try finding nearby brackets to speed up code
            d_needed = depth(code2[cut2:])
            while depth(code1[cut1:]) != d_needed and tmp < 10:
                cut1 += 1
                tmp += 1

            new1 = repair(code1[cut1:] + code2[:cut2])
            new2 = repair(code2[cut2:] + code1[:cut1])

            g1_out = run(new1, trainer.gen_in())
            fitness1 = trainer.check_fitness(g1_out)
            g2_out = run(new2, trainer.gen_in())
            fitness2 = trainer.check_fitness(g2_out)

            if fitness1 != float('inf') and fitness2 != float('inf'):
                valid = True

        return new1, new2

    # TODO: Call the above mutations in varying amounts
    if bool(random.getrandbits(1)):
        output = translocation(code1, code2)
    else:
        output = (deletion(code1), duplication(code2))

    return output

