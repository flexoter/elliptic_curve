#!/usr/bin/sudo python
# -*- coding: utf-8 -*-
"""
    Module contains probabilistic functions
    that could be usefull in elliptic cryptography

"""

from collections import (
    defaultdict,
    namedtuple
)
from sympy import mod_inverse
from math import sqrt
from random import (
    randint,
    seed
)
from .simplicityTests import (
    ferma_test,
    find_point_representation,
    root_computation
)


def find_discriminant(a_value, b_value, field):

    """
    Function finds an discriminant of an elliptic curve of the following form:
    y^2 = x^3 + a*x + b
    Discriminant may be found with next formula:
    4*a^3 + 27*b^2
    Possible values: int(1), int(0), int(-1)

    :param int a_value: x coefficient
    :param int b_value: free member
    :param int field: an a curve field

    """

    return (4 * int(pow(a_value, 3, field)) + 27 *
            int(pow(b_value, 2, field))) % field


def create_point(x_crd, y_crd):

    """
    Function creates a point as a namedtuple type\n

    :param int x_crd: x point cooedinate\n
    :param int y_crd: y point cooedinate\n

    """

    Point = namedtuple("Point", "x_crd y_crd")
    return Point(x_crd, y_crd)


def is_point_exist(point, a_value, b_value, field):

    """
    Function determines whether a point belongs an a elliptic curve
    defined by the following cubic function (y^2 = x^3 + a*x + b) or not\n
    Possible values: True, False\n

    :param int a_value: x coefficient\n
    :param int b_value: free member\n
    :param int field: an a curve field\n
    :param int rounds: iteration number (optional)\n

    """

    return (
            (point.y_crd ** 2 - (point.x_crd ** 3 + a_value * point.x_crd + b_value)) % field == 0 and
            0 <= point.x_crd < field and 0 <= point.y_crd < field)


def is_curve_exist(a_value, b_value, field, rounds=7, m='eq'):

    """
    Function determines whether an elliptic curve defined by the
    following cubic function (y^2 = x^3 + a*x + b) is exist\n
    Possible values: True, ValueError, "Given field is not an a simple number",
                           ValueError, "Given curve doesn't exist"

    :param int a_value: x coefficient\n
    :param int b_value: free member\n
    :param int field: an a curve field\n
    :param int rounds: iteration number (optional)\n

    """

    # Checking if given field is a simple value
    if m != 'eq':
        if ferma_test(field, rounds) is not True:
            raise ValueError("Given field is not an a simple number")

    # Find discriminant to ensure that a curve exist
    if find_discriminant(a_value, b_value, field) == 0:
        return False
    else:
        return True


def find_ordinate(x_value, a_value, b_value, field):

    """
    Function finds an a point's ordinate by given x_value\n
    Possible values: 0 .. field - 1\n


    :param int x_value: x coordinate\n
    :param int a_value: an a value in elliptic form E(a, b)\n
    :param int b_value: an b value in elliptic form E(a, b)\n
    :param int field: an a curve field\n

    """

    # y_value may be found by simple substitution of x_value in the equation
    return (int(pow(x_value, 3, field)) + a_value * x_value + b_value) % field


def find_points(a_value, b_value, field):

    """
    Function finds elliptic curve points that actually exist\n
    by using Euler's criterion to establish whether found point
    x coordinate is quadratic deducation and Tonelli-Shenks algorythm
    for root computation\n
    Returns an a defaultdict structure that contains points coordinates
    in the following form:\n
    x0: [y01, (y02)]\n
    x1: [y11, (y12)]\n
    ................\n
    x(field - 1): [y(field - 1)1, (y(field - 1)2)]\n

    :param int a_value: an a value in elliptic form E(a, b)\n
    :param int b_value: an b value in elliptic form E(a, b)\n
    :param int field: an a curve field\n

    """

    # Initialize dict of points that will store points coordinates
    points_dict = defaultdict(list)

    for x_value in range(field):
        # Find an y_value with find_ordinate function
        y_value = find_ordinate(x_value, a_value, b_value, field)
        # If found y_value^2 is 0 then add point immediately
        if y_value == 0:
            points_dict[x_value].append(y_value)
        else:
            try:
                # In other case calculate a root modulo and find y_value
                roots = root_computation(y_value, field)
                for point in roots:
                    # Add found points to the points dict
                    points_dict[x_value].append(point)
            # Try | except statement in case function finds an unexisting point
            except TypeError:
                pass

    return points_dict


def inverse_modulo(value, field):
    """
    Compute an inverse for x modulo p, assuming that x
    is not divisible by p.
    """
    print("i_m", value)
    if value % field == 0:
        raise ZeroDivisionError("Impossible inverse")
    return int(pow(value, field - 2, field))


def possible_devide(devinder, devider, field):

    devinder %= field
    devider %= field

    while devinder % devider != 0:
        devinder += field
        devider += field

    return devinder / devider


def add_points(f_point, s_point, field, a_value, b_value):

    """
    Function finds a sum of a given points\n
    Points is set in the tuple structure of the following form:
    (x_coord, y_coord)\n
    Returns an a tuple of the same structure\n
    Possible values: tuple([rx_value, ry_value]),
                     ValueError, "Denominator can not be equal zero",
                     ValueError (In case point at infinity)\n

    :param tuple f_point: tuple that contains coordinates\n
    of the first given point
    :param tuple s_point: tuple that contains coordinates\n
    of the second given point
    :param int field: an a curve field\n
    :param int a_value: an a value in elliptic form E(a, b)\n
    (optinal, it is required in case summ of the same point)

    """

    if not (is_point_exist(f_point, a_value, b_value, field) and is_point_exist(s_point, a_value, b_value, field)):
        raise ValueError("Given point don't belong to elliptic curve")

    # Initialize coordinates of the result point
    rx_value = int()
    ry_value = int()

    # Find a sum of a given points
    if f_point == s_point:
        alpha = (3 * f_point.x_crd ** 2 + a_value) * mod_inverse(2 * f_point.y_crd, field)
    else:
        alpha = (s_point.y_crd - f_point.y_crd) * mod_inverse(s_point.x_crd - f_point.x_crd, field)
    # Find a sum of a given points
    rx_value = (alpha ** 2 - f_point.x_crd - s_point.x_crd) % field
    ry_value = (alpha * (f_point.x_crd - rx_value) - f_point.y_crd) % field

    return create_point(rx_value, ry_value)


def multiply_point(point, multiplier, field, a_value, b_value):

    """
    Function finds a composition of a given point on given multiplier\n
    Point is set in the tuple structure of the following form:\n
    (x_coord, y_coord)\n
    Returns an a tuple of the same structure\n
    Possible values: tuple([rx_value, ry_value]),
                     -1, "Got an a point at infinity"\n

    :param tuple point: tuple that contains coordinates of the given point\n
    :param int multiplier: int coefficient\n
    :param int field: an a curve field\n
    :param int a_value: an a value in elliptic form E(a, b)\n
    (optinal, it is required in case summ of the same point)

    """

    s_point = add_points(point, point, field, a_value, b_value)
    multiplier -= 2

    # Find out how much 2P we must add further
    while multiplier != 0:
        multiplier -= 1
        try:
            s_point = add_points(s_point, point, field, a_value, b_value)    
        except ValueError:
            raise ValueError("Got a point an eternity...")

    return s_point


def find_point_order(point, field, a_value, b_value):
    """
    Function finds an order of a given point\n
    Order in this case is max factor by multiply on which
    we get point on eternity\n
    Point is set in the tuple structure of the following form:\n
    (x_coord, y_coord)\n
    Returns an int\n
    Possible values: int(),

    :param tuple point: tuple that contains coordinates of the given point\n
    :param int field: an a curve field\n
    :param int a_value: an a value in elliptic form E(a, b)\n
    :param int a_value: an b value in elliptic form E(a, b)\n

    """
    order = int(2)
    try:
        s_point = add_points(point, point, field, a_value, b_value)
    except ValueError:
        return order
    while True:
        try:
            s_point = add_points(s_point, point, field, a_value, b_value)
            order += 1
        except ValueError:
            return order

def diffy_hellman(field, a_value, b_value, point):
    """
    Function performs DF-algorythm on given elliptic curve\n
    DF-algorythm step-by-step:\n
    1. Field and point parameteres need to be established by user
    2. A-side generate alpha-factor in field
    3. B-side generate beta-factor in field
    4. A-side finds result of multiplying alpha-factor and given point and send it to B-side
    5. B-side finds result of multiplying beta-factor and given point and send it to A-side
    6. A-side finds common secret key by multiplying alpha-facror on gotten from B-side point
    7. B-side finds common secret key by multiplying beta-facror on gotten from A-side point
    8. If common secret keys are the same on both sides algorythm ends up.
       In another case common secret key generation will require to repeat DF-algorythm
    Point is set in the tuple structure of the following form:\n
    (x_coord, y_coord)\n
    Returns a common secret key in a Point form\n
    Possible values: tuple([key_x, key_y]),
                    ValueError("Got a point an eternity...")

    :param tuple point: tuple that contains coordinates of the given point\n
    :param int field: an a curve field\n
    :param int a_value: an a value in elliptic form E(a, b)\n
    :param int a_value: an b value in elliptic form E(a, b)\n

    """
    a_comb, b_comb = int(), int()
    while a_comb == b_comb:
        a_comb = randint(1, sqrt(field) // 2)
        b_comb = randint(1, sqrt(field) // 2)
    print("Next factors have been generated:")
    print("alhpha: ", a_comb)
    print("beta: ", b_comb)
    try:
        a_point = multiply_point(point, a_comb, field, a_value, b_value)
        b_point = multiply_point(point, b_comb, field, a_value, b_value)
        a_secret = multiply_point(b_point, a_comb, field, a_value, b_value)
        b_secret = multiply_point(a_point, b_comb, field, a_value, b_value)
    except ValueError:
        print("Got a point an eternity... Please, repeat DF-algorythm")
        return
    if a_secret != b_secret:
        print("Something has terribly gone wrong...")
        return
    else:
        print("Common secret key has been succesfully generated")
        return a_secret


if __name__ == "__main__":
    pass
