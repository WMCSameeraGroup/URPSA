from atoms.atoms import Atom
from settings import stop_distance_factor, input_file_directory


def make_atoms_from_input_file(file, n_origin_atoms):
    data = read_com(file).split("\n\n")
    atoms_strings = data[1].split('\n')[3:]
    atoms = []
    for atom_string in atoms_strings:
        atoms.append(Atom(*atom_string.split()))
    return atoms[0:n_origin_atoms], atoms[n_origin_atoms:]


def read_com(file):
    if "/" in file:  # if full path is given
        with open(file, 'r') as com:
            return com.read()
    else:
        with open(input_file_directory + '/' + file, 'r') as com:
            return com.read()


def is_too_close(origin_atoms, moving_atoms):
    for i in origin_atoms:
        for j in moving_atoms:

            if i.distance_between(j) < (i.v_radius + j.v_radius)*stop_distance_factor: # stop distance is 0.2 of sum of vandaval radius
                print(i.distance_between(j), i, j)
                return False
    return True


def is_not_highly_repulsive(file, n_origin_atoms):
    moving_atoms,origin_atoms = make_atoms_from_input_file(file,n_origin_atoms)
    return is_too_close(moving_atoms,origin_atoms)



#is_not_highly_repulsive("../inputFiles/Test4.com",3)
