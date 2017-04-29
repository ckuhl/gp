import random


def visualize_control_chars(s):
    """
    Format a string to remove all literals, replacing them with their pictoral symbol
    :param s: string to substitute
    :return: substituted string
    """
    # TODO: Add in rest of https://en.wikipedia.org/wiki/C0_and_C1_control_codes
    return s.replace('\0', '␀')\
            .replace('\a', '␇')\
            .replace('\b', '␈')\
            .replace('\f', '␌')\
            .replace('\n', '␊')\
            .replace('\r', '␍')\
            .replace('\t', '␉')\
            .replace('\v', '␋')


def weighted_choice(tuple_list):
    """
    Makes a weighted selection from a list of tuples
    :param tuple_list: List of tuples, of the form [(weight, item), ...]
    :return:
    """
    total = sum([x[0] for x in tuple_list])
    interval_tuples = [tuple((x[0] / total, x[1])) for x in tuple_list]

    choice = random.random()
    choice -= interval_tuples[0][0]
    while choice > 0:
        interval_tuples = interval_tuples[1:]
        choice -= interval_tuples[0][0]
    return interval_tuples[0][1]

