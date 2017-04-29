import random


def gen_root_set(min_v, max_v):
    """
    Return a set of coefficients for a root form quadratic formula
      `(qx+p)(rx+s)=0`
    """
    q, p, r, s = (random.randint(min_v, max_v) for x in range(4))
    return (q, p, r, s)


def gen_std_form(root_set):
    """
    Given a root set of the form (p, q, r, s), return the standard form
      coefficients of a quadratic equation (i.e. return (a, b, c) of the quadratic
      equation: `ax^2+bx+c=0`
    """
    a = root_set[0] * root_set[2]
    b = -1 * (root_set[0] * root_set[3] + root_set[1] * root_set[2])
    c = root_set[1] * root_set[3]
    return (a, b, c)


def gen_quadratic_eqn(root_set):
    """
    Generate a quadratic equation from the generated roots
    """
    a, b, c = gen_std_form(root_set)
    return lambda x: (a*x**2 + b*x + c)
