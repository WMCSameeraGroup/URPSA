from atoms.atoms import Atom
from calculations.random_spherical_coords_generator import random_spherical_coordinates_generator, \
    equidistributed_points_generator
from molecule.molecule import Molecule
from inputFileParser import CustomConfigParser


class InputFile:

    def __init__(self, file):
        self.file = file
        self.config = CustomConfigParser()
        self.config.read(self.file)
        self.project_name = self.config.get('project', 'project_name')
        self.sphere_radius = int(self.config.get('controls', 'sphere_radius'))
        self.step_size = float(self.config.get('controls', 'step_size'))
        self.step_count = int(self.config.get('controls', 'step_count'))
        self.stop_distance_factor = float(self.config.get('controls', 'stop_distance_factor'))
        self.charge = int(float(self.config.get('molecules', 'charge')))
        self.multiplicity = int(float(self.config.get('molecules', 'multiplicity')))
        self.number_of_molecules = int(self.config.get('molecules', 'number_of_molecules'))
        self.n_iterations = int(self.config.get('controls', 'n_iterations'))
        # self.rotation_random = "random" in self.data.split("\n\n")[4].split()
        # self.rotation_step = self.set_rotation_step()
        self.spherical_placement = self.config.get('controls', 'spherical_placement')
        self.method = self.config.get('gaussian', 'method')
        self.cores = self.config.get('gaussian', 'number_of_cores')
        self.memory = self.config.get('gaussian', 'memory')

        self.list_of_molecules = self.set_molecule_list()
        # update with
        self.update_with_optimized_coordinates = self.config.get('controls', 'update_with_optimized_coordinates')
        self.is_placed_on_sphere = self.create_spherically_located_molecule_list()

    def set_molecule_list(self):
        molecule_list = []
        for n in range(self.number_of_molecules):
            string = self.config.get('molecules', str(n))
            molecule_list.append(self.set_molecule(string))

        self.list_of_molecules =molecule_list
        return molecule_list

    def set_molecule(self, string):
        atom_list = []
        for line in string.split("\n"):
            line_data = line.split()
            if len(line_data) >= 4:  # linear convergence
                atom_list.append(Atom(*line_data))
            else:
                print("incorrect format in inputfile ")
        return Molecule(atom_list)


    def create_spherically_located_molecule_list(self):

        if self.spherical_placement == "False":
            return False
        for molecule in self.list_of_molecules:
            if self.spherical_placement == "Total_random":
                molecule.update_coordinates(*random_spherical_coordinates_generator(self.sphere_radius))
            elif self.spherical_placement == "statistically_even":
                molecule.update_coordinates(*equidistributed_points_generator(self.sphere_radius))
        return True


if __name__ == "__main__":
    print(InputFile('exampleInput.txt').list_of_molecules)
