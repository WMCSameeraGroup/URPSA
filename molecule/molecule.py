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
        return rotated_xyz

    def rotation_yz(self, angle):
        rot_mat = np.array([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]])
        rotated_xyz = np.dot(self.xyz, rot_mat.T)
        return rotated_xyz

    def rotation_xz(self, angle):
        rot_mat = np.array([[np.cos(angle), 0, np.sin(angle)], [0, 1, 0], [-np.sin(angle), 0, np.cos(angle)]])
        rotated_xyz = np.dot(self.xyz, rot_mat.T)
        return rotated_xyz

    def translation_x(self, distance):
        translated_xyz = self.xyz + np.array([distance, 0, 0])
        return translated_xyz

    def translation_y(self, distance):
        translated_xyz = self.xyz + np.array([0, distance, 0])
        return translated_xyz

    def translation_z(self, distance):
        translated_xyz = self.xyz + np.array([0, 0, distance])
        return translated_xyz
