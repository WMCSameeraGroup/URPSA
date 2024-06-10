from inputFileGeneration.input_file_writer import file_name_generator, setup_input_file
from inputFileGeneration.input_template import get_input_template
from inputFileGeneration.write_input_file import generate_input_file
from settings import method, number_of_cores


class System:

    def __init__(self, charge, multiplicity):
        self.molecules = []
        self.charge = charge
        self.multiplicity = multiplicity
        self.number_of_atoms = self.cal_number_of_atoms()

    def add_molecule(self, molecule):
        self.molecules.append(molecule)

    def cal_number_of_atoms(self):
        count = 0
        for molecule in self.molecules:
            count += len(molecule.atoms)
        self.number_of_atoms = count
        return count

    def generate_input_file(self, number):
        """write input file in the inputFiles dir """
        string_of_coordinates = self.get_string_of_atoms_and_coordinates()
        template_str = get_input_template(number, self, calc_method=method, num_of_cores=number_of_cores)
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

    #
    def set_moleculer_coordinates(self, opt_xyz):
        """change molecules to new optimized coordinates """
        count = 0
        for molecule in self.molecules:
            n_atoms = molecule.number_of_atoms()
            molecule.xyz = opt_xyz[count: n_atoms + count]
            molecule.cal_gravity_point()
            count += n_atoms
            molecule.setAtomNewCoords()

    def to_str(self):
        string = f"{self.cal_number_of_atoms()}\n"
        for molecule in self.molecules:
            string += molecule.to_str() + "\n"
        return string


