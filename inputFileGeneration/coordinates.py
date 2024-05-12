import numpy as np
from calculations.gravitypoint import gravity_point


def relative_coordination_matrix(atoms):
    xyz_matrix = np.array([atom.get_coords() for atom in atoms])
    relative_atom_coords = xyz_matrix - gravity_point(atoms)
    return relative_atom_coords


def update_atoms(atoms, matrix):
    for i, j in zip(atoms, matrix):
        i.update_coordinates(*j)


def coordinate_generation(atom_list, step_count, step_size):
    list_of_coordinates = []
    # change atom coords with gravity point
    matrix = relative_coordination_matrix(atom_list)
    for i in range(step_count):
        x_matrix = np.array([[1, 0, 0] for _ in range(len(atom_list))])
        position_matrix = matrix + x_matrix * i * step_size
        list_of_coordinates.append(position_matrix)
    return list_of_coordinates


def string_of_atoms_coordinates(atoms, atom_coordinates):
    str = ""
    atom_symbols = [atom.symbol for atom in atoms]
    for symbol, xyz in zip(atom_symbols, atom_coordinates):
        atom_str_line = f"{symbol} {xyz[0]:.2f} {xyz[1]:.2f} {xyz[2]:.2f}\n"
        str += atom_str_line
    return str


