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
