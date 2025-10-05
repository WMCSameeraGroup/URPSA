import math
from random import uniform
from utils.unit_converters import hatree2kjmol

from PIL.ImImagePlugin import number

from calculations.random_spherical_coords_generator import random_spherical_coordinates_generator, \
    generate_random_point_on_sphere
from inputFileGeneration.input_file_writer import file_name_generator
from inputFileGeneration.input_template import get_input_template
from inputFileGeneration.write_input_file import generate_input_file


class System:
    """ System class contains all the molecules in the system and their properties
    :Attributes:
    molecules (list): list of Molecule objects in the system
    charge (int): total charge of the system
    multiplicity (int): total multiplicity of the system
    method (str): method to be used in the calculation
    number_of_cores (int): number of cores to be used in the calculation
    iteration (int): current iteration number
    energy (float): total energy of the system
    memory (int): memory to be used in each calculation
    stress_release (list): list of iteration numbers where stress release is applied
    additional_constraints (str): additional constraints to be added to the input file
    controls (Controls): Controls object containing all the control parameters
    lattice (Lattice): Lattice object containing the lattice parameters
    number_of_atoms (int): total number of atoms in the system

    """

    def __init__(self, controls):
        self.molecules = []
        self.charge = controls.charge
        self.multiplicity = controls.multiplicity
        self.method = controls.method
        self.number_of_cores = controls.cores
        self.iteration = 0
        self.energy = 0.0
        self.memory = controls.memory
        self.stress_release = controls.stress_release
        self.additional_constraints = controls.additional_constraints
        self.controls = controls
        self.lattice = controls.lattice
        self.number_of_atoms = self.cal_number_of_atoms()

    def add_molecule(self, molecule):
        """ add a molecule to the system
        :param molecule: Molecule
            molecule to be added to the system
        """
        self.molecules.append(molecule)

    def replace_molecules(self, molecules):
        """ replace the molecules in the system with new molecules
        :param molecules: list of Molecule
        list of new molecules to be added to the system"""
        self.remove_all_molecules()
        self.add_list_of_molecules(molecules)

    def add_list_of_molecules(self, list):
        """ add a list of molecules to the system
        :param list: list of Molecule
        list of molecules to be added to the system"""
        self.molecules += list

    def remove_all_molecules(self):
        """ remove all molecules from the system """
        self.molecules = []

    def reorient_molecules_to_start(self):
        """ reorient all molecules to their initial orientation """
        for molecule in self.molecules:
            molecule.reorient_molecule_to_start()

    def cal_number_of_atoms(self):
        """ calculate the total number of atoms in the system
        :return: int
            total number of atoms in the system
        """
        count = 0
        for molecule in self.molecules:
            count += len(molecule.atoms)
        self.number_of_atoms = count
        if self.lattice:
            count += len(self.lattice.atoms)
        return count

    def list_of_atoms(self):
        """ return a list of all atoms in the system
        :return: list of Atom
            list of all atoms in the system
        """
        atom_list = []

        for molecule in self.molecules:
            atom_list.extend(molecule.atoms)
        atom_list=sorted(atom_list, key=lambda atom: atom.number)
        return atom_list

    def add_keyword_to_method(self, keyword):
        """ add a keyword to the method if it is not already present
        this is useful for adding OPT or FREQ keywords to the method
        :param keyword: str
            keyword to be added to the method
        :return: bool
            True if the keyword was added, False if it was already present
        """
        if keyword not in self.method.lower():
            self.method += " "+ keyword
            return True
        return False

    def remove_keyword_from_method(self, keyword):
        """ remove a keyword from the method if it is present
        :param keyword: str
            keyword to be removed from the method
        """
        self.method = self.method.replace(keyword, "")

    def generate_input_file(self, iter_num, input_file_directory):
        """writing an input file is controlled in this method
        :param iter_num: int
            current iteration number
        :param input_file_directory: str
            directory where the input file will be written
        :return: str
            name of the input file
        """
        string_of_coordinates = self.get_string_of_atoms_and_coordinates()
        template_str = get_input_template(iter_num, self, input_file_directory)
        file_name = file_name_generator(iter_num)
        com_constraints = self.add_additinal_constrains(iter_num)
        string_to_be_written = self.additional_gaussian_requirments_implementation_to_inputfile_str(
            string_of_coordinates, template_str, com_constraints)
        generate_input_file(file_name, input_file_directory, string_to_be_written)
        return file_name

    def get_string_of_atoms_and_coordinates(self):
        """ get the string of atoms and coordinates in the system
        :return: str
            string of atoms and coordinates in the system
        """
        atoms_and_coordinates = ""
        atom_list=[]
        for atom in self.list_of_atoms():
            atom_list.append(atom)
        for atom in atom_list:
            atoms_and_coordinates += str(atom) + "\n"

        if self.lattice:
            return atoms_and_coordinates + self.lattice.to_str() + "\n"
        return atoms_and_coordinates[:-1]

    def additional_gaussian_requirments_implementation_to_inputfile_str(self, string, template, other=""):
        """ add additional requirements to the input file string
        :param string: str
            string of atoms and coordinates in the system
        :param template: str
            input file template
        :param other: str
            additional constraints to be added to the input file
        :return: str
            string to be written in the input file
        """
        return template + string + other + "\n\n\n\n"

    def set_moleculer_coordinates(self, opt_xyz):
        """
        Update the molecular coordinates of all molecules in the system to new optimized coordinates.

        This function iterates over each molecule in the system and replaces its current
        atomic coordinates with the corresponding optimized coordinates from the `opt_xyz` list.
        It also ensures that the new coordinates are set for each atom within the molecule.

        Parameters
        ----------
        opt_xyz : list of tuples
            A list containing the optimized (x, y, z) coordinates for all atoms in the system.
            The coordinates must be provided in the same order as the atoms in the system.

        Updates
        -------
        - Updates the `xyz` attribute of each molecule with the corresponding new coordinates.
        - Calls `set_new_coords_to_atoms()` on each molecule to propagate the changes to its atoms.

        Note
        ----
        The function assumes that `opt_xyz` contains coordinates for all atoms in all molecules
        in the correct order, and that the number of coordinates matches the total number of atoms
        across all molecules in the system.
        """
        for atom,coords in zip(self.list_of_atoms(),opt_xyz):
            atom.update_coordinates(*coords)


    def to_str(self):
        """ return a string representation of the system
        :return: str
        string representation of the system
        example:
        5
        Energy: -150.0
        C 0.0 0.0 0.0
        H 0.0 0.0 1.0
        H 1.0 0.0 0.0
        O 0.0 0.0 0.0
        H 0.0 0.0 1.0
        Lattice parameters...
        """
        string = f"{self.cal_number_of_atoms()}\nEnergy: {self.energy}\n"
        for atom in self.list_of_atoms():
            string += str(atom) + "\n"
        if self.lattice:
            string += self.lattice.to_str() + "\n"
        return string

    def string_optimized_coordinates(self, opt_xyz):
        """ return a string representation of the optimized coordinates used in xyz file
        1. number of atoms
        2. energy of the system
        3. list of atoms with their optimized coordinates
        4. lattice parameters if present
        5. return the string representation of the optimized coordinates
        :param opt_xyz: list of tuples
            list of optimized coordinates
        :return: str
            string representation of the optimized coordinates
        """
        # this is for the xyz file not input file
        string = f"{self.cal_number_of_atoms()}\nEnergy: {self.energy}\n"

        for atom in self.list_of_atoms():
            string += str(atom) + "\n"
        if self.lattice:
            string += self.lattice.to_str() + "\n"
        return string

    def set_scf_done(self, energy):
        """ set the energy of the system after scf is done
        :param energy: float
            energy of the system
        """
        self.energy = energy

    def re_orient_molecules(self, controls):
        """ re orient the molecules in the system
        :param controls: Controls
            Controls object containing all the control parameters
        :return: bool
            True if the molecules were re oriented, False otherwise
        """
        if controls.spherical_placement == "False":
            return False
        for molecule in self.molecules:
            if controls.spherical_placement == "Total_random":
                molecule.update_coordinates(*random_spherical_coordinates_generator(controls.sphere_radius))

            elif controls.spherical_placement == "statistically_even":
                molecule.update_coordinates(*generate_random_point_on_sphere(controls.sphere_radius))
                # molecule.print_center_of_mass()
        return True


    def random_rotate_molecules(self):
        """ randomly rotate all molecules in the system
        using euler angles from 0 to pi
        :return: None
        """

        for molecule in self.molecules:
            molecule.rotation_xy(uniform(0, math.pi)).rotation_yz(uniform(0, math.pi)).rotation_xz(uniform(0, math.pi))

    def add_additinal_constrains(self, number):
        """ add center of mass constrains using GIC
            def :  https://gaussian.com/gic/ ,
                    https://gaussian.com/geom/
                    https://mattermodeling.stackexchange.com/questions/12004/gaussian-16-relaxed-scan-using-jacobi-coordinates-expressed-using-generalized-i/12005#12005
        """
        string = "\n\n"

        if number in self.stress_release:
            return string
        elif self.additional_constraints:
            string += self.additional_constraints
            return string
        # todo: change this the architecture is bad if  ADD_COM_CONST is not their then default make it true
        elif self.controls.ADD_COM_CONST == "True":
            return self.constraints_generation(string)
        elif self.controls.ADD_SPHERICAL_CONST == "True":
            return self.spherical_constraints(string)
        elif self.controls.ADD_TRUE_COM == "True":
            return self.true_come_constraints(string)

    def spherical_constraints(self, string):
        def list_of_atoms(molecule1):
            """replace dash with comma if there are only 2 atoms in a molecule"""
            number_string = ""
            for atom in molecule1.atoms:
                number_string += f"{atom.number},"
            return number_string[0:-1]

        for n, molecule in enumerate(self.molecules):
            string += f"XCm{n + 1} (Inactive) = XCntr({list_of_atoms(molecule)}) \nYCm{n + 1} (Inactive) = YCntr({list_of_atoms(molecule)}) \nZCm{n + 1} (Inactive) = ZCntr({list_of_atoms(molecule)})\n"

        n_mol = len(self.molecules)
        for i in range(n_mol):
            i += 1
            string += f"radius{i}(FREEZE)=sqrt[(XCm{i})^2+(YCm{i})^2+(ZCm{i})^2]*0.529177\n"
        return string

    def constraints_generation(self, string):

        def list_of_atoms(molecule1):
            """replace dash with comma if there are only 2 atoms in a molecule"""
            number_string = ""
            for atom in molecule1.atoms:
                number_string += f"{atom.number},"
            return number_string[0:-1]

        for n, molecule in enumerate(self.molecules):
            string += f"XCm{n + 1} (Inactive) = XCntr({list_of_atoms(molecule)}) \nYCm{n + 1} (Inactive) = YCntr({list_of_atoms(molecule)}) \nZCm{n + 1} (Inactive) = ZCntr({list_of_atoms(molecule)})\n"

        n_mol = len(self.molecules)
        for i in range(n_mol - 1):
            i += 1
            for j in range(n_mol - i):
                j += 1
                string += f"F{i}F{i + j}(FREEZE)=sqrt[(XCm{i}-XCm{i + j})^2+(YCm{i}-YCm{i + j})^2+(ZCm{i}-ZCm{i + j})^2]*0.529177\n"
        return string

    def true_come_constraints(self, string):
        def list_of_atoms(molecule1):
            x_string = "("
            y_string = "("
            z_string = "("
            sum_of_mass = 0
            for atom in molecule1.atoms:
                sum_of_mass += atom.mass
            for atom in molecule1.atoms:
                x_string += f"{atom.mass}*X({atom.number})+"
                y_string += f"{atom.mass}*Y({atom.number})+"
                z_string += f"{atom.mass}*Z({atom.number})+"
            x_string = x_string[0:-1] +f")*{0.529177/sum_of_mass}"
            y_string = y_string[0:-1] +f")*{0.529177/sum_of_mass}"
            z_string = z_string[0:-1] +f")*{0.529177/sum_of_mass}"
            return x_string, y_string , z_string


        for n, molecule in enumerate(self.molecules):
            string += f"XCm{n + 1} (Inactive) = {list_of_atoms(molecule)[0]} \nYCm{n + 1} (Inactive) = {list_of_atoms(molecule)[1]} \nZCm{n + 1} (Inactive) = {list_of_atoms(molecule)[2]}\n"

        n_mol = len(self.molecules)
        for i in range(n_mol - 1):
            i += 1
            for j in range(n_mol - i):
                j += 1
                string += f"F{i}F{i + j}(FREEZE)=sqrt[(XCm{i}-XCm{i + j})^2+(YCm{i}-YCm{i + j})^2+(ZCm{i}-ZCm{i + j})^2]*0.529177\n"
        return string

    def set_list_of_atom_symbols(self):
        return [a.symbol for a in self.list_of_atoms()]


    def get_energy_gap(self,energy_iter1,energy_iter2):
        """ get the energy gap between two iterations in kj/mol
        :param energy_iter1: float
        energy of the first iteration in hartree
        :param energy_iter2: float
        energy of the second iteration in hartree
        :return: float
        energy gap between the two iterations in kj/mol
        """
        try:
            energy_iter1 =float(energy_iter1)
            energy_iter2 = float(energy_iter2)
        except ValueError:
            print("Error with your input file check gaussian log files ")
            return 0
        energy_gap_in_hartree = energy_iter2 - energy_iter1
        to_kj_mol = hatree2kjmol(energy_gap_in_hartree)
        return to_kj_mol



