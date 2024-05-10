from random import uniform


def random_spherical_coordinates_generator(r: float):
    """ function generates coordinates that fits to the equation X^2 + Y^2 + Z^2 = R^2
    when input parameter radius was given """
    x = uniform(-r, r)
    y_max = (r ** 2 - x ** 2) ** 0.5
    y = uniform(-y_max, y_max)
    z = (r**2 - x ** 2 - y ** 2) ** 0.5
    return x, y, z


