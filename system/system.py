from calculations.random_spherical_coords_generator import random_spherical_coordinates_generator, \
    equidistributed_points_generator
from inputFileGeneration.input_file_writer import file_name_generator, setup_input_file
from inputFileGeneration.input_template import get_input_template
from inputFileGeneration.write_input_file import generate_input_file



class System:

    def __init__(self, charge, multiplicity, method, cores):
        self.molecules = []
        self.charge = charge
        self.multiplicity = multiplicity
        self.method = method
        self.number_of_cores = cores
        self.number_of_atoms = self.cal_number_of_atoms()

    def add_molecule(self, molecule):
        self.molecules.append(molecule)

    def add_list_of_molecules(self, list):
        self.molecules += list

    def cal_number_of_atoms(self):
        count = 0
        for molecule in self.molecules:
            count += len(molecule.atoms)
        self.number_of_atoms = count
        return count

    def generate_input_file(self, number):
        """write input file in the inputFiles dir """
        string_of_coordinates = self.get_string_of_atoms_and_coordinates()
        template_str = get_input_template(number, self, self.method, self.number_of_cores)
        file_name = file_name_generator(number)
        string_to_be_written = self.additional_gaussian_requirments_implementation_to_inputfile_str(
            string_of_coordinates, template_str)
        generate_input_file(file_name, string_to_be_written)
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
            temp_molecule_gravity_point = molecule.gravity_point
            molecule.xyz = opt_xyz[count: n_atoms + count]
            molecule.change_gravity_point(temp_molecule_gravity_point)
            count += n_atoms


    def to_str(self):
        string = f"{self.cal_number_of_atoms()}\nEnergy: {self.energy}\n"
        for molecule in self.molecules:
            string += molecule.to_str() + "\n"
        return string


    def set_scf_done(self,energy):
        self.energy = energy

    def re_orient_molecules(self, controls):
        if controls.spherical_placement == "False":
            return False
        for molecule in self.molecules:
            if controls.spherical_placement == "Total_random":
                molecule.update_coordinates(*random_spherical_coordinates_generator(controls.sphere_radius))
            elif controls.spherical_placement == "statistically_even":
                molecule.update_coordinates(*equidistributed_points_generator(controls.sphere_radius))
        return True



    def change_orientations_of_molecules(self, controls):
        if controls.spherical_placement == "False":
            return False
        for molecule in self.molecules:
            if controls.change_orientation == "Total_random":
                molecule.update_coordinates(*random_spherical_coordinates_generator(controls.sphere_radius))
            elif controls.change_orientation == "statistically_even":
                molecule.update_coordinates(*equidistributed_points_generator(controls.sphere_radius))
        return True