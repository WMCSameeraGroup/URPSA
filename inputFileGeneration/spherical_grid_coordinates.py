"""

"""
import numpy as np
from atoms.atoms import Atom


def spherically_converge_atom(atom: Atom, size=1):
    """
    initial position (x0,y0,z0) is the initial position vector
    to move the atom in the opposite direction of the position vector (towards origin)
    unit_vector is multiplied by the size and reduced from the position vector
    this will give the new position of the atom.
    :param atom:
    :param size:
    :return [x, y, z]:
    """
    position_vector = np.array(atom.get_coords())
    unit_vector = np.array(atom.unit_position_vector())
    new_position = position_vector - size * unit_vector
    atom.update_coordinates(*new_position)
    return new_position


def move_atoms_towards_center(molecule, size):
    for atom in molecule.atoms:
        spherically_converge_atom(atom, size)


def spherical_gird_coordinate_generation(molecule, step_count, step_size):
    """
    this functions converges atoms to the origin

    :param molecule:
    :param step_count:
    :param step_size:
    :return:
    """
    list_of_coordinates = []

    for i in range(step_count):
        coordinates_of_atoms = molecule.get_coordinates_of_atoms()
        list_of_coordinates.append(coordinates_of_atoms)
        move_atoms_towards_center(molecule, step_size)
    return list_of_coordinates


if __name__ == "__main__":
    print(spherically_converge_atom(Atom("Si", 1, 1, 1)))
