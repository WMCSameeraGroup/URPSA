"""

"""
import numpy as np
from atoms.atoms import Atom
from molecule.molecule import Molecule


def spherically_converge_to_center(molecule, size=1):
    """
    initial position (x0,y0,z0) is the initial position vector
    to move the atom in the opposite direction of the position vector (towards origin)
    unit_vector is multiplied by the size and reduced from the position vector
    this will give the new position of the molecule or the atom.
    :param atom:
    :param size:
    :return [x, y, z]:
    """
    position_vector = np.array(molecule.get_coords())
    unit_vector = np.array(molecule.unit_position_vector())
    new_position = position_vector - size * unit_vector
    molecule.update_coordinates(*new_position)
    return new_position


def move_atoms_towards_center(molecule, size):
    for atom in molecule.atoms:
        spherically_converge_to_center(atom, size)


def spherical_gird_coordinate_generation(molecules, step_count=1, step_size=1):
    """
    this functions converges atoms to the origin

    :param molecules:
    :param List:
    :param step_count:
    :param step_size:
    :return:
    """

    for i in range(step_count):
        for molecule in molecules:
            spherically_converge_to_center(molecule, step_size)



if __name__ == "__main__":
    print(spherically_converge_to_center(Molecule([Atom("Si", 1, 1, 1)])))
