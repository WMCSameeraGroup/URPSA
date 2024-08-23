import numpy as np
from calculations.gravitypoint import gravity_point


class Molecule:
    atoms = []
    xyz = []

    def __init__(self, list_of_atoms, *args):
        self.atoms = list_of_atoms
        self.xyz = np.array([atom.get_coords() for atom in self.atoms])
        self.gravity_point = self.cal_gravity_point()
        self.x = self.gravity_point[0]
        self.y = self.gravity_point[1]
        self.z = self.gravity_point[2]

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

    def cal_gravity_point(self):
        gp= gravity_point(self.atoms)
        self.x = gp[0]
        self.y = gp[1]
        self.z = gp[2]
        return gp

    def to_str(self):
        str = ""
        for atom in self.atoms:
            str += atom.__str__() + "\n"
        return str[:-1]

    def __str__(self):
        return self.to_str()

    def get_coords(self):
        return self.gravity_point

    def update_coordinates(self, x, y, z):
        """update coordinates of atoms with movement of gravity point"""

        new_gravity_point = [x, y, z]
        change_in_gravity_points = np.array(new_gravity_point) - np.array(self.gravity_point)
        self.translation_x(change_in_gravity_points[0])
        self.translation_y(change_in_gravity_points[1])
        self.translation_z(change_in_gravity_points[2])
        self.gravity_point = self.cal_gravity_point()


    def relative_coordination_matrix(self):
        xyz_matrix = np.array([atom.get_coords() for atom in self.atoms])
        relative_atom_coords = xyz_matrix - gravity_point(self.atoms)
        return relative_atom_coords

    def change_gravity_point(self, gravity_point):
        """ change the molecule coordinates without the bond distances and angles"""
        self.xyz = self.relative_coordination_matrix() + gravity_point
        self.cal_gravity_point()
        self.setAtomNewCoords()




    def distance_between(self, other):
        diff_x = pow(self.x - other.x, 2)
        diff_y = pow(self.y - other.y, 2)
        diff_z = pow(self.z - other.z, 2)
        return pow(diff_z + diff_x + diff_y, 0.5)

    def unit_position_vector(self):
        magnitude = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
        return [self.x / magnitude, self.y / magnitude, self.z / magnitude]

    def distance_from_origin(self):
        diff_x = pow(self.x, 2)
        diff_y = pow(self.y, 2)
        diff_z = pow(self.z, 2)
        return pow(diff_z + diff_x + diff_y, 0.5)

    def calculate_RMSD(self):
        ref_atom = self.atoms[0]
        sum_of_distances_square = 0
        for atom in self.atoms[1:]:
            sum_of_distances_square += ref_atom.distance_between(atom)**2

        return (sum_of_distances_square/len(self.atoms))**0.5

    def reorient_molecule_to_start(self):
        for atom in self.atoms:
            atom.reorient_atom_to_start()
        self.cal_gravity_point()