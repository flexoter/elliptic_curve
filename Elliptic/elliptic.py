"""
    Module contains probabilistic functions
    that could be usefull in elliptic cryptography

"""

from collections import defaultdict
from random import randint, seed
from numpy import array
from simplicityTests import ferma_test, find_point_representation, root_computation


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

    return (4 * (a_value ** 3) + 27 * (b_value ** 2)) % field


def is_curve_exist(a_value, b_value, field, rounds=None):

    """
    Function determines whether an elliptic curve defined by the 
    following cubic function (y^2 = x^3 + a*x + b) is exist:
    Possible values: True, ValueError, "Given field is not an a simple number",
                           ValueError, "Given curve doesn't exist"

    :param int a_value: x coefficient
    :param int b_value: free member
    :param int field: an a curve field
    :param int rounds: iteration number (optional)

    """

    # Initializing round value for simplicity test
    r = int(7)
    if rounds is not None:
        r = rounds

    # Checking if given field is a simple value
    if ferma_test(field, r) is not True:
        return ValueError, "Given field is not an a simple number"

    # Find discriminant to ensure that a curve exist
    if find_discriminant(a_value, b_value, field) == 0:
        return ValueError, "Given curve doesn't exist"
    else:
        return True


def find_ordinate(x_value, a_value, b_value, field):

    """
    Function finds an a point's ordinate by given x_value
    Possible values: 0 .. field - 1


    :param int x_value: x coordinate
    :param int a_value: an a value in elliptic form E(a, b)
    :param int b_value: an b value in elliptic form E(a, b)
    :param int field: an a curve field

    """

    # y_value may be found by simple substitution of x_value in the equation
    return (x_value**3 + a_value*x_value + b_value) % field


def find_points(a_value, b_value, field):

    """
    Function finds elliptic curve points that actually exist
    by using Euler's criterion to establish whether found point 
    x coordinate is quadratic deducation and Tonelli-Shenks algorythm
    for root computation
    Returns an a defaultdict structure that contains points coordinates in the following form:
    x0: [y01, (y02)]
    x1: [y11, (y12)]
    ................
    x(field - 1): [y(field - 1)1, (y(field - 1)2)]

    :param int a_value: an a value in elliptic form E(a, b)
    :param int b_value: an b value in elliptic form E(a, b)
    :param int field: an a curve field

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


def add_points(f_point, s_point, field, a_value=None):

    """
    Function finds a sum of a given points
    Points is set in the tuple structure of the following form (x_coord, y_coord)
    Returns an a tuple of the same structure
    Possible values: tuple([rx_value, ry_value]),
                     ValueError, "Denominator can not be equal zero",
                     ValueError (In case point at infinity)

    :param tuple f_point: tuple that contains coordinates of the first given point
    :param tuple s_point: tuple that contains coordinates of the first given point
    :param int field: an a curve field
    :param int a_value: an a value in elliptic form E(a, b) (optinal, it is required in case summ of the same point)

    """

    # Initialize coordinates of the result point
    rx_value = int()
    ry_value = int()

    # Find a sum of a given points
    if f_point[0] == s_point[0] and f_point[1] == s_point[1]:
        if f_point[1] == 0:
            return ValueError, "Denominator can not be equal zero"
        rx_value = ((((3 * f_point[0] ** 2 + a_value) % field) // 2 * f_point[1]) ** 2 - 2 * f_point[0]) % field
        ry_value = (-f_point[1] + (((3 * f_point[0] ** 2 + a_value) % field) // ((2 * f_point[1]) % field)) * (f_point[0] - rx_value)) % field
    else:
        try:
            rx_value = ((((s_point[1] - f_point[1]) % field) // (s_point[0] - f_point[0]) % field) ** 2 - (f_point[0] + s_point[0])) % field
            ry_value = (-f_point[1] + (((s_point[1] - f_point[1]) % field) // (s_point[0] - f_point[0]) % field) * (f_point[0] - rx_value)) % field
        except ZeroDivisionError:
            return ValueError

    return tuple([rx_value, ry_value])


def multiply_point(point, multiplier, field, a):

    """
    Function finds a composition of a given point on given multiplier
    Point is set in the tuple structure of the following form (x_coord, y_coord)
    Returns an a tuple of the same structure
    Possible values: tuple([rx_value, ry_value]),
                     -1, "Got an a point at infinity"

    :param tuple point: tuple that contains coordinates of the given point
    :param int multiplier: int coefficient
    :param int field: an a curve field
    :param int a_value: an a value in elliptic form E(a, b) (optinal, it is required in case summ of the same point)

    """

    # Find out how much 2P we must add further
    d_value, r_value = find_point_representation(multiplier)
    # Find 2P point
    d_point = add_points(point, point, field, a_value=a)
    # If multiplier is more than 2 find P + 2P
    if d_value > 1:
        s_point = add_points(d_point, d_point, field, a_value=a)
    else:
        # In other case if r_value is 0 then return 2P point
        if r_value == 0:
            return d_point
        else:
            # In other case return P + 2P point
            return add_points(d_point, point, field, a_value=a)
    for _ in range(d_value):
        try:
            # Consistently add points
            s_point = add_points(s_point, d_point, field)
        # Try | except statement in case function finds an a point at infinity
        except TypeError:
            return -1, "Got an a point at infinity"
    if r_value != 0:
        # In other case if r_value is not 0 then return P + 2P point
        s_point = add_points(s_point, point, field)
    return s_point


if __name__ == "__main__":
    pass


