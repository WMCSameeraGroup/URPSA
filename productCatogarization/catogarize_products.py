from atoms.atoms import Atom
from molecule.molecule import Molecule


def save_products():
    """
    todo:saving
    need to save input orientation, products observed and their RMSDs
    :return:
    """
    pass


def get_products_list(symbols,output_file_list):
    if len(output_file_list)>0:
        add_products(symbols,output_file_list)
    else:
        print("no output file is produced")

def get_atom_list(symbols, opt_coords):
    atomList = []
    xyz = opt_coords
    for symbol, atom in zip(symbols, xyz):
        atomList.append(Atom(symbol, *atom))

    return atomList



def add_products(atom_symbols, outputfile_list):
    index = find_the_formation_of_products(outputfile_list)
    atom_list = get_atom_list(atom_symbols, outputfile_list[index].opt_coords)
    molecules = get_molecules(atom_list)
    for molecule in molecules:
        print(f"setp-{index} RMSD- {molecule.calculate_RMSD()}")


def find_the_formation_of_products(file_list):
    """ find the minimum energy point"""
    minimum_index = 0
    i = 0
    for j,i in enumerate(file_list):
        if i.is_converged == 0 and i.scf_done <= file_list[minimum_index].scf_done:
            minimum_index = j
        j += 1
    return minimum_index


def get_molecules(atomlist, factor=1):
    list_of_molecules = []

    while len(atomlist) > 0:
        molecule = Molecule([atomlist[0]])
        atomlist.pop(0)

        no_more_atoms_to_add = False

        while len(atomlist) > 0 and not no_more_atoms_to_add:
            no_more_atoms_to_add = True
            to_remove = []

            for atom_in_molecule in molecule.atoms:
                for alone_atom in atomlist:
                    # Assuming each atom has a method distance_between() and a property v_radius
                    if atom_in_molecule.distance_between(alone_atom) < factor * (
                            atom_in_molecule.v_radius + alone_atom.v_radius):
                        to_remove.append(alone_atom)
                        no_more_atoms_to_add = False

            # Add the atoms to the molecule and remove them from atomlist
            for atom in to_remove:
                molecule.add_atom(atom)
                if atom in atomlist:
                    atomlist.remove(atom)  # Ensure atom is in atomlist before attempting to remove

        list_of_molecules.append(molecule)

    return list_of_molecules
