import math
from random import uniform

from PIL.ImImagePlugin import number

from calculations.random_spherical_coords_generator import random_spherical_coordinates_generator, \
    equidistributed_points_generator
from inputFileGeneration.input_file_writer import file_name_generator
from inputFileGeneration.input_template import get_input_template
from inputFileGeneration.write_input_file import generate_input_file


class System:

    def __init__(self, controls):
        self.molecules = []
        self.charge = controls.charge
        self.multiplicity = controls.multiplicity
        self.method = controls.method
        self.number_of_cores = controls.cores
        self.number_of_atoms = self.cal_number_of_atoms()
        self.iteration = 0
        self.energy = 0.0
        self.memory = controls.memory
        self.stress_release = controls.stress_release
        self.additinal_constraints = controls.additional_constraints
        self.controls = controls

    def add_molecule(self, molecule):
        self.molecules.append(molecule)

    def replace_molecules(self, molecules):
        print(molecules)
        self.remove_all_molecules()
        self.add_list_of_molecules(molecules)

    def add_list_of_molecules(self, list):
        self.molecules += list

    def remove_all_molecules(self):
        self.molecules = []

    def reorient_molecules_to_start(self):
        for molecule in self.molecules:
            molecule.reorient_molecule_to_start()

    def cal_number_of_atoms(self):
        count = 0
        for molecule in self.molecules:
            count += len(molecule.atoms)
        self.number_of_atoms = count
        return count

    def list_of_atoms(self):
        atom_list = []

        for molecule in self.molecules:
            atom_list.extend(molecule.atoms)
        return atom_list

    def generate_input_file(self, number, input_file_directory):
        """write input file in the inputFiles directory """
        string_of_coordinates = self.get_string_of_atoms_and_coordinates()
        template_str = get_input_template(number, self, input_file_directory)
        file_name = file_name_generator(number)
        com_constraints = self.add_additinal_constrains(number)
        string_to_be_written = self.additional_gaussian_requirments_implementation_to_inputfile_str(
            string_of_coordinates, template_str, com_constraints)
        generate_input_file(file_name, input_file_directory, string_to_be_written)
        return file_name

    def get_string_of_atoms_and_coordinates(self):
        atoms_and_coordinates = ""
        for molecule in self.molecules:
            atoms_and_coordinates += molecule.to_str() + "\n"

        return atoms_and_coordinates[:-1]

    def additional_gaussian_requirments_implementation_to_inputfile_str(self, string, template, other=""):
        return template + string + other + "\n\n\n\n"

    def set_moleculer_coordinates(self, opt_xyz):
        """change molecules to new optimized coordinates """
        count = 0
        for molecule in self.molecules:
            n_atoms = molecule.number_of_atoms()
            molecule.xyz = opt_xyz[count: n_atoms + count]
            molecule.setAtomNewCoords()
            count += n_atoms

    def to_str(self):
        string = f"{self.cal_number_of_atoms()}\nEnergy: {self.energy}\n"
        for molecule in self.molecules:
            string += molecule.to_str() + "\n"
        return string

    def string_optimized_coordinates(self, opt_xyz):
        count = 0
        string = f"{self.cal_number_of_atoms()}\nEnergy: {self.energy}\n"

        def to_str(symbols, coords):
            str = ""
            for symbol, coord in zip(symbols, coords):
                str += f"{symbol} {coord[0]} {coord[1]} {coord[2]}\n"
            return str

        for molecule in self.molecules:
            list_of_atom_symbols = [a.symbol for a in molecule.atoms]
            n_atoms = molecule.number_of_atoms()
            string += to_str(list_of_atom_symbols, opt_xyz[count: n_atoms + count])
            count += n_atoms
        return string

    def set_scf_done(self, energy):
        self.energy = energy

    def re_orient_molecules(self, controls):
        if controls.spherical_placement == "False":
            return False
        for molecule in self.molecules:
            if controls.spherical_placement == "Total_random":
                molecule.update_coordinates(*random_spherical_coordinates_generator(controls.sphere_radius))

            elif controls.spherical_placement == "statistically_even":
                molecule.update_coordinates(*equidistributed_points_generator(controls.sphere_radius))
                # molecule.print_center_of_mass()
        return True

    # def change_orientations_of_molecules(self, controls):
    #     if controls.spherical_placement == "False":
    #         return False
    #     for molecule in self.molecules:
    #         if controls.change_orientation == "Total_random":
    #             molecule.update_coordinates(*random_spherical_coordinates_generator(controls.sphere_radius))
    #         elif controls.change_orientation == "statistically_even":
    #             molecule.update_coordinates(*equidistributed_points_generator(controls.sphere_radius))
    #     return True

    def random_rotate_molecules(self):

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
        elif self.additinal_constraints and self.controls.ADD_COM_CONST == "True":
            string += self.additinal_constraints
            return string

        def list_of_atoms(molecule1):
            """replace dash with comma if there are only 2 atoms in a molecule"""
            number_string = ""
            for atom in molecule1.atoms:
                number_string += f"{atom.number},"
            return number_string[0:-1]

        for n, molecule in enumerate(self.molecules):
            string += f"XCm{n+1} (Inactive) = XCntr({list_of_atoms(molecule)}) \nYCm{n+1} (Inactive) = YCntr({list_of_atoms(molecule)}) \nZCm{n+1} (Inactive) = ZCntr({list_of_atoms(molecule)})\n"

        n_mol = len(self.molecules)
        for i in range(n_mol - 1):
            i += 1
            for j in range(n_mol - i):
                j += 1
                string += f"F{i}F{i + j}(FREEZE)=sqrt[(XCm{i}-XCm{i + j})^2+(YCm{i}-YCm{i + j})^2+(ZCm{i}-ZCm{i + j})^2]*0.529177\n"
        return string

    def set_list_of_atom_symbols(self):
        return [a.symbol for a in self.list_of_atoms()]
