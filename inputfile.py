from atoms.atoms import Atom
from calculations.random_spherical_coords_generator import random_spherical_coordinates_generator


class InputFile:

    def __init__(self, file):
        self.file = file
        self.data = self.read_file()
        self.sphere_radius = self.set_radius()
        self.atom_list = self.set_atom_list()
        self.step_size = float(self.data.split("\n\n")[1].split()[0])
        self.step_count = int(float(self.data.split("\n\n")[1].split()[1]))
        self.charge = int(float(self.data.split("\n\n")[3].split()[0]))
        self.multiplicity = int(float(self.data.split("\n\n")[3].split()[1]))
        self.origin_molecule = self.set_origin_molecule()
        self.origin_atoms = self.set_origin_atom_list()
        self.n_iter = self.set_n_iter()
        self.rotation_random = "random" in self.data.split("\n\n")[4].split()
        self.rotation_step = self.set_rotation_step()

    def set_atom_list(self):
        atom_list = []
        for line in self.data.split("\n\n")[0].split("\n"):
            line_data = line.split()
            if len(line_data) >= 4:  # linear convergence
                atom_list.append(Atom(*line_data))
            elif len(line_data) >= 2:  # spherical convergence
                atom_list += self.create_spherically_located_atom_list(line_data)
            else:
                print("incorrect format in inputfile ")
        return atom_list

    def read_file(self):
        with open(self.file, 'r') as file:
            return file.read()

    def set_origin_atom_list(self):
        atom_list = []
        for line in (self.data.split("\n\n")[2].split("\n")[1:]):
            line_data = line.split()
            if len(line_data) >= 4:  # linear convergence
                atom_list.append(Atom(*line_data))
            else:  # spherical convergence
                return []
        return atom_list

    def create_spherically_located_atom_list(self, line_data):
        atom_list = []

        for times in range(int(line_data[1])):
            atom_list.append(Atom(line_data[0], *random_spherical_coordinates_generator(self.sphere_radius)))
        return atom_list

    def set_radius(self):
        if "radius" in self.data.split("\n\n")[4].split():
            print(self.data.split("\n\n")[4].split())
            return int(self.data.split("\n\n")[4].split()[1])
        return 10

    def set_n_iter(self):
        if not "radius" in self.data.split("\n\n")[4].split():
            return int(float(self.data.split("\n\n")[4].split()[0]))
        else:
            return 1

    def set_rotation_step(self):
        if not "radius" in self.data.split("\n\n")[4].split():
            return [float(i) for i in self.data.split("\n\n")[4].split()[2:]]
        else:
            [0.0, 0.0, 0.0]

    def set_origin_molecule(self):
        if not "radius" in self.data.split("\n\n")[4].split():
            return self.data.split("\n\n")[2][1:]
        else:
            return ''
