import numpy as np


class Molecule:
    atoms = []
    xyz = []

    def __init__(self, list_of_atoms, *args):
        self.atoms = list_of_atoms
        self.xyz = np.array([atom.get_coords() for atom in self.atoms])

    def rotation_xy(self, angle):
        rot_mat = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
        rotated_xyz = np.dot(self.xyz, rot_mat.T)  # Transpose of the rotation matrix for proper multiplication
        self.xyz = rotated_xyz
        self.setAtomNewCoords()
        return self

    def rotation_yz(self, angle):
        rot_mat = np.array([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]])
        rotated_xyz = np.dot(self.xyz, rot_mat.T)
        self.xyz = rotated_xyz
        self.setAtomNewCoords()
        return self

    def rotation_xz(self, angle):
        rot_mat = np.array([[np.cos(angle), 0, np.sin(angle)], [0, 1, 0], [-np.sin(angle), 0, np.cos(angle)]])
        rotated_xyz = np.dot(self.xyz, rot_mat.T)
        self.xyz = rotated_xyz
        self.setAtomNewCoords()
        return self

    def translation_x(self, distance):
        translated_xyz = self.xyz + np.array([distance, 0, 0])
        self.xyz = translated_xyz
        self.setAtomNewCoords()
        return self

    def translation_y(self, distance):
        translated_xyz = self.xyz + np.array([0, distance, 0])
        self.xyz = translated_xyz
        self.setAtomNewCoords()
        return self

    def translation_z(self, distance):
        translated_xyz = self.xyz + np.array([0, 0, distance])
        self.xyz = translated_xyz
        self.setAtomNewCoords()
        return self

    def setAtomNewCoords(self):
        for atom, coords in zip(self.atoms, self.xyz):
            atom.update_coordinates(*coords)

    def get_coordinates_of_atoms(self):
        return np.array([atom.get_coords() for atom in self.atoms])

    def add_atom(self, atom):
        self.atoms.append(atom)

    def number_of_atoms(self):
        return len(self.atoms)