from atoms.atoms import Atom


class InputFile:

    def __init__(self, file):
        self.file = file
        self.data = self.read_file()
        self.atom_list = self.set_atom_list()
        self.step_size = float(self.data.split("\n\n")[1].split()[0])
        self.step_count = int(float(self.data.split("\n\n")[1].split()[1]))
        self.charge = int(float(self.data.split("\n\n")[3].split()[0]))
        self.multiplicity = int(float(self.data.split("\n\n")[3].split()[1]))
        self.origin_molecule = self.data.split("\n\n")[2][1:]
        self.origin_atoms = self.set_origin_atom_list()

    def set_atom_list(self):
        atom_list = []
        for line in self.data.split("\n\n")[0].split("\n"):
            line_data = line.split()
            atom_list.append(Atom(*line_data))
        return atom_list

    def read_file(self):
        with open(self.file, 'r') as file:
            return file.read()


    def set_origin_atom_list(self):
        atom_list = []
        for line in (self.data.split("\n\n")[2].split("\n")[1:]):
            line_data = line.split()
            atom_list.append(Atom(*line_data))
        return atom_list




