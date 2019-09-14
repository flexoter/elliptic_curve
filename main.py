"""
    Main module is supposed to run the Elliptic programm 

"""

from sys import exit
from matplotlib import pyplot as plt
from numpy import ogrid
from sympy import mod_inverse
from Elliptic.elliptic import (
    is_curve_exist,
    find_points,
    add_points,
    multiply_point,
    find_ordinate,
    create_point,
    is_point_exist,
    diffy_hellman
)
from Elliptic.simplicityTests import root_computation


def system_cls(idention=100):
    """
    
    Function moves the cursor for a number of characters specified by\n
    given "indention" parameter\n

    :param int idention: an a value of indention\n

    """

    for _ in range(idention):
        print()


def show_curve(a_value, b_value, field, point_dict):

    """
    Function draw a graph of elliptic curve with given parameteres\n

    :param int a_value: an a value in elliptic form E(a, b)\n
    :param int b_value: an b value in elliptic form E(a, b)\n
    :param int field: an a curve field\n
    :param defaultdict point_dict: an a dict that contains point's coordinates\n

    """

    # Initialize 2D-axis for plt.show() 
    y_axis, x_axis = ogrid[-field:field:4, -field:field:4]
    # Set function equal
    elliptic_func = y_axis ** 2 - x_axis ** 3 - x_axis * a_value - b_value
    show_lvl = [1]

    # plt.plot(x_coord, y_coord, "o") for plot points
    plt.contour(x_axis.ravel(), y_axis.ravel(), elliptic_func, show_lvl)
    plt.title("Elliptic curve E" + str(field) + "(" + str(a_value) + " " + str(b_value) + ")")
    plt.grid()
    plt.show()


def main():

    """
    Main function that requires elliptic curve parameteres and
    definds whether given elliptic curve exists and then give user a choise:\n
    -> find curve points\n
    -> find points summ\n
    -> find points multiply\n
    -> show plot\n
    -> exit\n

    """
    try:
        a, b, field = map(int, input("Enter elliptic curve parameteres: ").split(" "))
    except ValueError:
        print("Please, enter correct values...\nExit of a programm")
        exit(33)
    if is_curve_exist(a, b, field) is True:
        points_dict = find_points(a, b, field)
        print("Curve is actually exist")
        print()
        while True:
            print("\n\n\nPress 1 to output dict of elliptic curve points")
            print("Press 2 to perform adding of points")
            print("Press 3 to perform multiplying of point")
            print("Press 4 to show elliptic curve function graph")
            print("Press 5 to perform diffy-hellman protocol")
            print("Press 6 to exit of program")
            try:
                option = int(input("Choose the program option: "))
            except ValueError:
                print("Please, enter correct values...\nExit of a programm")
                continue
            print()
            if option == 1:
                print("Requested dict of points:")
                print("x | y")
                for key in points_dict:
                    print(key, points_dict[key])
                _ = input("Tap if you want to continue program execution")
                system_cls(150)
            elif option == 2:
                try:
                    x, y = map(int, input("Enter first point coordinates: ").split(" "))
                    f_point = create_point(x, y)
                    x, y = map(int, input("Enter second point coordinates: ").split(" "))
                    s_point = create_point(x, y)
                except ValueError:
                    print("Please, enter correct values...")
                    print("Exit of a programm")
                    system_cls(150)
                    continue
                try:
                    r_point = add_points(f_point, s_point, field, a, b)
                except ValueError:
                    print("Given point doesn't belong to elliptic curve")
                    system_cls(150)
                    continue
                print("Result point: ", r_point)
                _ = input("Tap if you want to continue program execution")
                system_cls(150)
            elif option == 3:
                try:
                    x, y = map(int, input("Enter point coordinates: ").split(" "))
                    f_point = create_point(x, y)
                    multiplier = int(input("Enter an multiplier: "))
                except ValueError:
                    print("Please, enter correct values...\nExit of a programm")
                    system_cls(150)
                    continue
                try:
                    r_point = multiply_point(f_point, multiplier, field, a, b)
                except ValueError:
                    print("Given point doesn't belong to elliptic curve")
                    system_cls(150)
                    continue
                print("Result point: ", r_point)
                _ = input("Tap if you want to continue program execution")
                system_cls(150)
            elif option == 4:
                show_curve(a, b, field, points_dict)
                _ = input("Tap if you want to continue program execution")
                system_cls(150)
            elif option == 5:
                x, y = map(int, input("Enter existing elliptic point coordinates: ").split(" "))
                point = create_point(x, y)
                print(diffy_hellman(field, a, b, point))
            elif option == 6:
                print("Exiting of program execution...Good luck!")
                exit(33)


if __name__ == "__main__":
    main()
