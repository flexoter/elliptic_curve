"""
    Module contains probabilistic simplicity tests functions
    that determine whether given value is an a simple value\n

"""

from collections import namedtuple
from random import randint, seed
from numpy import array

# Compound numbers that hard to identify correctly by probabilistic algorythms 
CARMICHAEL_NUMBERS = list([561, 1105, 1729, 2465, 2821, 6601, 8911, 10585,
                          15841, 29341, 41041, 46657, 52633, 62745,
                          63973, 75361])


def gcd(a_value, b_value):

    """
    Function finds an gcd of a pair of given numbers.\n

    :param int a_value: first value\n
    :param int n_value: second value\n

    """

    if a_value < b_value:
        a_value, b_value = b_value, a_value

    while b_value:

        a_value, b_value = b_value, a_value % b_value

    return a_value


def euler_criterion(a_value, field):

    """
    Function finds Euler criterion which determine whether given number
    is deduction on given field.\n
    Possible values: True, False, ValueError\n

    :param int a_value: given number to find deduction\n
    :param int field: simple value which is usually field\n

    """

    criterion = int(pow(a_value, (field - 1) // 2, field))

    if criterion == 1:
        return True
    elif criterion - field == -1:
            return False
    else:
        return ValueError, "Given number is defenitely not deduction\n"


def find_representation(value):

    """
    Function finds a (2**s_value)*t_value format number representation
    which is required in miller_rabin_test.\n

    :param int value: number represestation of which is required\n

    """

    s_value = int()

    if value % 2 != 0:
        value -= 1

    while value % 2 == 0:
        value /= 2
        s_value += 1

    return s_value, int(value)


def find_point_representation(value):

    return value // 2, value % 2


def ferma_test(simple_value, rounds):

    """
    Function determines whether given value is a simple or not
    with Ferma algorythm.\n
    Possible values: True, False, ValueError, "Error message"\n

    :param int simple_value: number that will be checked on simplicity\n
    :param int rounds: check iteration number\n

    """

    if simple_value == 2 or simple_value == 3:
        return True

    if simple_value in CARMICHAEL_NUMBERS:
        return False

    # Seeding randint function for clear number randomizing
    seed(randint(1, 2048))

    if simple_value == 1:
        return ValueError, "1 is neither an a simple or compound number"

    # Checking if given simple value is odd
    if simple_value % 2 is 0:
        return ValueError, "Given number is even"

    # Perform multiple rounds of division
    for _ in range(rounds):
        random_simple = int(0)
        while gcd(random_simple, simple_value) != 1:
            random_simple = randint(2, simple_value)
        # Numpy array approach for performing big-integer operations
        if int(pow(random_simple, simple_value - 1, simple_value)) != 1:
            return False
        else:
            continue

    return True


def nightingale_strassen_test(simple_value, rounds):

    """
    Function determines whether given value is a simple or not
    with Nightingale-Strassen algorythm.\n
    Possible values: True, False, ValueError, "Error message"\n

    :param int simple_value: number that will be checked on simplicity\n
    :param int rounds: check iteration number\n

    """

    if simple_value == 2 or simple_value == 3:
        return True

    if simple_value in CARMICHAEL_NUMBERS:
        return False

    # Seeding randint function for clear number randomizing
    seed(0)

    if simple_value == 1:
        return ValueError, "1 is neither an a simple or compound number"

    # Checking if given simple value is odd
    if simple_value != 2:
        if simple_value % 2 is 0:
            return ValueError, "Given number is even"

    # Perform multiple rounds of division
    for _ in range(rounds):
        random_simple = int(0)
        while gcd(random_simple, simple_value) != 1:
            random_simple = randint(2, simple_value)
        devinder = array([random_simple ** ((simple_value - 1) // 2)],
                         dtype='object')
        remaider = devinder % array([simple_value])
        yakoby_symb = int(euler_criterion(devinder, simple_value))
        if remaider != yakoby_symb:
            return False
        else:
            continue

    return True


def miller_rabin_test(simple_value, rounds):

    """
    Function determines whether given value is a simple or not
    with Miller-Rabin algorythm.\n
    Possible values: True, False, ValueError, "Error message"\n

    :param int simple_value: number that will be checked on simplicity\n
    :param int rounds: check iteration number\n

    """

    if simple_value == 2 or simple_value == 3:
        return True

    if simple_value is CARMICHAEL_NUMBERS or simple_value == 0:
        return False

    # Seeding randint function for clear number randomizing
    seed(randint(1, 2048))

    if simple_value == 1:
        return ValueError, "1 is neither an a simple or compound number"

    # Checking if given simple value is odd
    if simple_value % 2 is 0:
        return ValueError, "Given number is even"

    # Find double representation of given simple value
    repeats, t_value = find_representation(simple_value - 1)

    # Perform multiple rounds of division
    for _ in range(rounds):

        simplicity_witness = False
        random_simple = int(0)
        while gcd(random_simple, simple_value) != 1:
            random_simple = randint(2, simple_value)
        primary_check = int(pow(random_simple, t_value, simple_value))
        if primary_check == 1 or primary_check == -1:
            return True
        for deuce_degree in range(repeats):
            remaider = int(pow(random_simple, (2 ** deuce_degree) * t_value, 
                               simple_value))
            # Given value is compound
            if remaider == 1:
                return False
            # Given value may be simple | Go to the next iteration
            elif remaider == simple_value - 1 or remaider == -1:
                simplicity_witness = True
                break

    return simplicity_witness


def find_quadratic_noncall(field):

    """
    Function finds a minimal quadratic non deduction of a given field.\n
    Possible values: 2 .. field - 1\n

    :param int field: an a curve field

    """

    for deducation in range(2, field):
        # Euler criterion says that if result value is 1 then found number
        # is deducation
        # In other case if result value is -1 then found number
        # is not deducation
        if euler_criterion(deducation, field) is False:
            return deducation


def find_minimal_deduction(t_value, m_value, field):

    """
    Function finds a minimal quadratic deduction of a given field.\n
    Possible values: 2 .. field - 1\n

    :param int t_value: an a t value in Tonelli-Shenks algorythm\n
    :param int m_value: an a m value in Tonelli-Shenks algorythm
    that is search limit\n
    :param int field: an a curve field\n

    """

    for dedon in range(1, m_value):
        if int(pow(t_value, int(pow(2, dedon, field)), field)) == 1:
            return dedon


def root_computation(value, field):

    """
    Function finds a root of a given value by given field\n
    with Tonelli-Shenks algorythm.\n Possible values:
        1 .. field - 1\n

    :param int value: value from which a root is required\n
    :param int field: an a curve field

    """

    r_value = int()
    min_denon = int()
    Point = namedtuple("Point", "x_crd y_crd")

    if euler_criterion(value, field) is not True:
        return ValueError("Given value is not mutually simple with field")

    s_value, q_value = find_representation(field)

    if (field % 4) == 3:
        r_value = int(pow(value, (field + 1) // 4, field))
        return Point(r_value, -r_value % field)

    z_value = find_quadratic_noncall(field)
    c_value = int(pow(z_value, q_value, field))
    r_value = int(pow(value, (q_value + 1) // 2, field))
    t_value = int(pow(value, q_value, field))
    m_value = s_value

    while t_value != 1:
        if m_value < 3:
            min_denon = 1
        else:
            min_denon = find_minimal_deduction(t_value, m_value, field)
        b_value = int(pow(c_value, int(pow(2, m_value - min_denon - 1, field)),
                          field))
        r_value = (r_value * b_value) % field
        t_value = (t_value * int(pow(b_value, 2, field))) % field
        c_value = int(pow(b_value, 2, field))
        m_value = min_denon

    return Point(r_value, -r_value % field)


if __name__ == "__main__":
    print(root_computation(2, 41))
