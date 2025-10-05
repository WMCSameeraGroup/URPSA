from atoms.atoms import Atom
from molecule.molecule import Molecule


def get_molecules(atomlist, factor=1.1):
    """ separate system into individual molecules"""
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
                    # Assuming if atoms are in the same molecule then atoms are closer than the sum of c_radius
                    # between their distance
                    if atom_in_molecule.distance_between(alone_atom) < factor * (
                            atom_in_molecule.c_radius + alone_atom.c_radius):
                        to_remove.append(alone_atom)
                        no_more_atoms_to_add = False

            # Add the atoms to the molecule and remove them from atomlist
            for atom in to_remove:
                molecule.add_atom(atom)
                if atom in atomlist:
                    atomlist.remove(atom)  # Ensure atom is in atomlist before attempting to remove

        list_of_molecules.append(molecule)
    return list_of_molecules





def get_new_molecules(atoms):
    return get_molecules(atoms)


class products_writer:
    """ write the products to products.txt file
    save number of atoms, RMSD, xyz coordinates for each molecule observed.
    and count the number of times the same products were observed
    which is used to exit the repeated calculations if the same products were observed over and over again.

    :Attributes:
        file (str): path to the products.txt file
        indent (int): indentation level for JSON formatting (default is 4)

    """
    def __init__(self, input_file_directory, file="products.txt"):
        self.file = input_file_directory + "/" + file

    def get_the_molecular_string(self, molecules):
        string = ''
        for molecule in molecules:
            string += f"{molecule.number_of_atoms()}\nRMSD {molecule.calculate_RMSD()}" + "\n" + molecule.to_str() + "\n"

        return string

    def save_products(self, molecules: [Molecule]):
        """
        save number of atoms, RMSD, xyz coordinates for each molecule observed.
        :return None:
        """
        string = self.get_the_molecular_string(molecules)
        self.write_products_file(string)

    def get_products_list(self, atoms, output_file_list):
        if len(output_file_list) > 0:
            return self.add_products(atoms, output_file_list)
        else:
            print("no output file is produced")

    def add_products(self, atoms, outputfile_list):
        index = self.find_the_formation_of_products(outputfile_list)
        molecules = get_molecules(atoms)
        for molecule in molecules:
            print(f"setp-{index} RMSD- {molecule.calculate_RMSD()}")

        self.save_products(molecules)
        return molecules

    def find_the_formation_of_products(self, file_list):
        """ find the last object"""
        return -1

    def create_if_not(self):
        try:
            with open(self.file, "a") as _:
                pass
        except:
            with open(self.file, "w") as _:
                pass

    def write_products_file(self, products):
        self.create_if_not()
        with open(self.file, "a") as f:
            f.write(products + "\n")

