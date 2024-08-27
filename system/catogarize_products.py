from atoms.atoms import Atom
from molecule.molecule import Molecule



def save_products():
    """
    need to save input orientation, products observed and RMSD
    :return:
    """
    pass


def get_atom_list(symbols, opt_coords):
    atomList= []
    xyz= opt_coords
    for symbol,atom in zip(symbols,xyz):
        atomList.append(Atom(symbol,*atom))

    return atomList


def add_products(atoms,outputfile_list):
    index=find_the_formation_of_products(outputfile_list)
    atom_list = get_atom_list(atoms, outputfile_list[index].opt_coords)
    molecules = find_products(atom_list)



def find_the_formation_of_products(file_list):
    """ find the minimum energy point"""
    minimum_index = 0
    i = 0
    while i < len(file_list):
        if i.is_converged == 0 and i.scd_done <= file_list[minimum_index].scf_done:
            minimum_index = i
        i += 1
    return minimum_index


def find_products(list_of_atoms, factor=1):
    molecules = []
    remaining_atoms = list_of_atoms[:]

    while remaining_atoms:
        ref_atom = remaining_atoms[0]
        molecule = Molecule([ref_atom])
        to_remove = []

        for atom in remaining_atoms[1:]:
            if ref_atom.distance_between(atom)*factor < atom.v_radius + ref_atom.v_radius:
                molecule.add_atom(atom)
                to_remove.append(atom)

        molecules.append(molecule)
        for atom in to_remove:
            remaining_atoms.remove(atom)
        remaining_atoms.remove(ref_atom)

    return molecules


# Test cases
def test_find_products():
    atom1 = Atom('H', 0, 0, 0)
    atom2 = Atom('H', 0, 0, 1)
    atom3 = Atom('O', 3, 0, 0)
    atom4 = Atom('O', 3, 0, 0.5)
    atom5 = Atom('C', 0, 10, 0)

    atoms = [atom1, atom2, atom3, atom4, atom5]

    molecules = find_products(atoms)
    for molecule in molecules:
        print(molecule)


    # Expected to form 3 molecules: one with two H atoms, one with two O atoms, and one with one C atom
    assert len(molecules) == 3, f"Expected 3 molecules, got {len(molecules)}"

    molecule_sizes = sorted([len(molecule.atoms) for molecule in molecules])

    assert molecule_sizes == [1, 2, 2], f"Expected molecule sizes [1, 2, 2], got {molecule_sizes}"

    print("All tests passed!")


#test_find_products()














