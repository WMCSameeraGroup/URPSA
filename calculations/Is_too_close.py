from atoms.atoms import Atom



def make_atoms_from_input_file(file, n_origin_atoms,input_file_directory):
    data = read_com(file,input_file_directory).split("\n\n")
    atoms_strings = data[1].split('\n')[3:]
    atoms = []
    for atom_string in atoms_strings:
        atoms.append(Atom(*atom_string.split()))
    return atoms[0:n_origin_atoms], atoms[n_origin_atoms:]


def read_com(file,input_file_directory):
    if "/" in file:  # if full path is given
        with open(file, 'r') as com:
            return com.read()
    else:
        with open(input_file_directory() + '/' + file, 'r') as com:
            return com.read()


def is_too_close(origin_atoms, moving_atoms, stop_distance_factor=0.5):
    for i in origin_atoms:
        for j in moving_atoms:

            if i.distance_between(j) < (
                    i.v_radius + j.v_radius) * stop_distance_factor:
                print(i.distance_between(j), i, j)
                return False
    return True


def is_not_highly_repulsive(file, n_origin_atoms):
    moving_atoms, origin_atoms = make_atoms_from_input_file(file, n_origin_atoms)
    return is_too_close(moving_atoms, origin_atoms)


################################### for spherical #####################################

def is_too_close_spherical(atoms1, atoms2, stop_distance_fac):
    """only atoms in 2 molecules are compered """
    for i in atoms1:
        for j in atoms2:
            if i.distance_between(j) < (
                    i.v_radius + j.v_radius) * stop_distance_fac:
                # check are they from the same molecule
                print(i.distance_between(j), i, j)
                return False
    return True




def is_not_highly_repulsive_spherically(sys, stop_distance_fac=0.5):
    """
    check the distance between atoms of different molecules
    """
    for molecule_1 in sys.molecules:
        for molecule_2 in sys.molecules:
            if molecule_2 == molecule_1:
                # if the same molecule
                continue
            if not is_too_close_spherical(molecule_2.atoms, molecule_1.atoms, stop_distance_fac):
                return False

    return True



