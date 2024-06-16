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

            if i.distance_between(j) < (
                    i.v_radius + j.v_radius) * stop_distance_factor:  # todo: stop distance is 0.2 change this by args of sum of vandaval radius
                print(i.distance_between(j), i, j)
                return False
    return True


def is_not_highly_repulsive(file, n_origin_atoms):
    moving_atoms, origin_atoms = make_atoms_from_input_file(file, n_origin_atoms)
    return is_too_close(moving_atoms, origin_atoms)


################################### for spherical #####################################

def is_too_close_spherical(atoms, stop_distance_fac):
    for i in atoms:
        for j in atoms:
            if i == j:  # in the case of same atom
                continue
            if i.distance_between(j) < (
                    i.v_radius + j.v_radius) * stop_distance_fac:  # todo: stop distance is 0.2 change this by args of sum of vandaval radius
                print(i.distance_between(j), i, j)
                return False
    return True


def is_not_highly_repulsive_spherically(file,stop_distance_fac=stop_distance_factor):
    """
     convert atoms in .com file to Atom objects using the function 1st return value is redundant
     then checked whether atoms are too close.
    """
    _, atoms = make_atoms_from_input_file(file, 0)
    return is_too_close_spherical(atoms, stop_distance_fac)



if __name__ == "__main__":
    print(is_not_highly_repulsive_spherically("../inputFiles/Test0.com"))
