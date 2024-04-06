import numpy as np

import atoms.atoms
import inputfile
from calculations.gravitypoint import gravity_point


#redundant
def generate_coordinates(atom='H', initial_cords_atom1=[10.0,0.0,0.0], initial_cords_atom2=[0.0,0.0,0.0], step_size=1, num_of_steps=10):
    """ returns the list of coordinates in string format"""
    list_of_coordinates = []
    for i in range(num_of_steps):
        new_coordinates = [initial_cords_atom1[0] - i * step_size, *initial_cords_atom1[1:]]
        coordinates = print_coordinates(atom, new_coordinates, initial_cords_atom2)
        list_of_coordinates.append(coordinates)
    return list_of_coordinates


def relative_coordination_matrix(atoms):
    xyz_matrix = np.array([atom.get_coords() for atom in atoms])
    relative_atom_coords = xyz_matrix - gravity_point(atoms)
    return relative_atom_coords

def update_atoms(atoms, matrix):
    for i,j in zip(atoms,matrix):
        i.update_coordinates(*j)

def coordinate_generation(atom_list, step_count, step_size):
    list_of_coordinates =[]
    # change atom coords with gravity point
    matrix = relative_coordination_matrix(atom_list)
    for i in range(step_count):
        x_matrix = np.array([[1,0,0] for _ in range(len(atom_list))])
        position_matrix = matrix + x_matrix*i * step_size

        # print(position_matrix)
        # todo: update atoms and check the distance then add
        list_of_coordinates.append(position_matrix)
    return list_of_coordinates

#redundant
def print_coordinates(atom, cords_atom1, cords_atom2):
    x1 = cords_atom1[0]
    y1 = cords_atom1[1]
    z1 = cords_atom1[2]
    x2 = cords_atom2[0]
    y2 = cords_atom2[1]
    z2 = cords_atom2[2]
    str = f"{atom} {x1} {y1} {z1} \n{atom} {x2} {y2} {z2} "

    return str

def string_of_atoms_coordinates(atoms, atom_coordinates):

    str=""
    atom_symbols = [atom.symbol for atom in atoms]
    for symbol, xyz  in zip(atom_symbols,atom_coordinates):
        atom_str_line =f"{symbol} {xyz[0]:.2f} {xyz[1]:.2f} {xyz[2]:.2f}\n"
        str += atom_str_line
    return str





#print(generate_coordinates())