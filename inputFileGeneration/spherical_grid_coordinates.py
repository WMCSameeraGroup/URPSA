"""

"""
import numpy as np
from atoms.atoms import Atom


def spherically_converge_atom(atom: Atom, size=1):
    position_vector = np.array(atom.get_coords())
    unit_vector = np.array(atom.unit_position_vector())
    new_position = position_vector - size * unit_vector
    atom.update_coordinates(*new_position)
    return new_position


def move_atoms_towards_center(molecule, size):
    for atom in molecule.atoms:
        spherically_converge_atom(atom, size)


def spherical_gird_coordinate_generation(molecule, step_count, step_size):
    list_of_coordinates = []

    for i in range(step_count):
        coordinates_of_atoms = molecule.xyz
        list_of_coordinates.append(coordinates_of_atoms)
        move_atoms_towards_center(molecule, step_size)
    return list_of_coordinates
