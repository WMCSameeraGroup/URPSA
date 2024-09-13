from atoms.atoms import Atom
from molecule.molecule import Molecule
from settings import input_file_directory


class products_writer:
    def __init__(self, file="products.txt"):
        self.file = input_file_directory + "/" + file

    def get_the_molecular_string(self, molecules):
        string = ''
        for molecule in molecules:
            string += f"{molecule.number_of_atoms()}\nRMSD {molecule.calculate_RMSD()}" +"\n"+ molecule.to_str() +"\n"

        return string

    def save_products(self,molecules: [Molecule]):
        """
        todo:saving this cant be saved in the input folder it needs to be there through out the
        need to save input orientation, products observed and their RMSDs
        :return:
        """
        string = self.get_the_molecular_string(molecules)
        self.write_products_file(string)




    def get_products_list(self, symbols, output_file_list):
        if len(output_file_list)>0:
            self.add_products(symbols,output_file_list)
        else:
            print("no output file is produced")

    def get_atom_list(self, symbols, opt_coords):
        atomList = []
        xyz = opt_coords
        for symbol, atom in zip(symbols, xyz):
            atomList.append(Atom(symbol, *atom))

        return atomList



    def add_products(self, atom_symbols, outputfile_list):
        index = self.find_the_formation_of_products(outputfile_list)
        atom_list = self.get_atom_list(atom_symbols, outputfile_list[index].opt_coords)
        molecules = self.get_molecules(atom_list)
        for molecule in molecules:
            print(f"setp-{index} RMSD- {molecule.calculate_RMSD()}")

        self.save_products(molecules)


    def find_the_formation_of_products(self,file_list):
        """ find the minimum energy point"""
        minimum_index = 0
        for j,i in enumerate(file_list):
            if i.is_converged == 0 and i.scf_done <= file_list[minimum_index].scf_done:
                minimum_index = j
            j += 1
        return minimum_index


    def get_molecules(self, atomlist, factor=1):
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


    def create_if_not(self):
        try:
            with open(self.file, "a") as _:
                pass
        except:
            with open(self.file, "w") as _:
                pass


    def write_products_file(self,products):
        self.create_if_not()
        with open(self.file, "a") as f:
            f.write(products + "\n")
