import random
from termcolor import cprint


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
            dptr -= 1
            try:
                data[dptr]
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


def gen(bounds):
    """
    Generate a random Brainfuck program

    :param bounds: (int, int) tuple containing min and max program length
    :return:  String containing a valid Brainfuck program
    """
    code = ''
    valid = False
    commands = ['>', '<', '+', '-', '.', ',', '[', ']']

    # Keep trying to make a string until we make one that works
    while not valid:
        code = ''
        while len(code) < bounds[0] or len(code) > bounds[1]:
            code += random.choice(commands)
        valid = validate(code)

    return code


def validate(code):
    """
    Performs trivial validation on a Brainfuck program

    :param code: String containing a valid Brainfuck program
    :return:  Whether or not the below program is valid
    """
    # check for balanced brackets
    lb, rb = code.count('['), code.count(']')
    if lb != rb:
        return False

    # check for paired brackets
    depth = 0
    for i in code:
        if i == '[':
            depth += 1
        elif i == ']':
            depth -= 1
        if depth < 0:
            return False

    return True


def mutate(code1, code2):
    """
    Mutate a given Brainfuck program in various ways
    :param code1: String, the subject program to mutate
    :param code2: String, the donor program to mutate
    :return: String, a mutated brainfuck program
    """
    # Delete a section of the program
    def deletion(code):
        pass

    # Duplicate a section of the program
    def duplication(code):
        pass

    # Invert a section of the program (e.g. abcdef -> abEDCf)
    def inversion(code):
        pass

    # Swap out code for it's complement (e.g. +/-, [/], >/<, ,/.)
    def complementation(code):
        pass

    # Delete a section of program one and insert it into program two
    def insertion(code1, code2):
        pass

    # Swap sections of program one and program 2
    def translocation(code1, code2):
        pass

    # TODO: Call the above mutations in varying amounts
    return translocation(code1, code2)
