import numpy as np
from calculations.center_of_mass import center_of_mass


class Molecule:
    atoms = []
    xyz = []

    def __init__(self, list_of_atoms, *args):
        """
            Initializes an object with a collection of atoms and calculates its properties.

            This constructor sets up the object using a list of atoms. It stores the
            coordinates of all atoms in a NumPy array, calculates the center of mass,
            and initializes the x, y, and z attributes to the center of mass coordinates.

            :param list_of_atoms: A list of `Atom` objects that make up the molecule or structure.
            :param args: Additional arguments (if any) to be passed for future extensions.
            :attribute atoms: Stores the input list of `Atom` objects.
            :attribute xyz: A NumPy array containing the coordinates of all atoms.
            :attribute center_of_mass: The center of mass of the collection of atoms, calculated upon initialization.
            :attribute x: The x-coordinate of the center of mass (float).
            :attribute y: The y-coordinate of the center of mass (float).
            :attribute z: The z-coordinate of the center of mass (float).
            """
        self.atoms = list_of_atoms
        self.xyz = np.array([atom.get_coords() for atom in self.atoms])
        self.center_of_mass = self.cal_center_of_mass()
        self.x = self.center_of_mass[0]
        self.y = self.center_of_mass[1]
        self.z = self.center_of_mass[2]

    def rotation_xy(self, angle: float):
        """
        Rotates the atom's position around the z-axis by a specified angle.
        :param angle:
        :return:
        """
        rot_mat = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
        rotated_xyz = np.dot(self.xyz, rot_mat.T)  # Transpose of the rotation matrix for proper multiplication
        self.xyz = rotated_xyz
        self.set_new_coords_to_atoms()
        return self


    def rotation_yz(self, angle: float):
        """
        Rotates the atom's position around the x-axis by a specified angle.
        :param angle:
        :return:
        """
        rot_mat = np.array([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]])
        rotated_xyz = np.dot(self.xyz, rot_mat.T)
        self.xyz = rotated_xyz
        self.set_new_coords_to_atoms()
        return self

    def rotation_xz(self, angle: float):
        """
        Rotates the: atom's position around the y-axis by a specified angle.
        :param angle:
        :return:
        """
        rot_mat = np.array([[np.cos(angle), 0, np.sin(angle)], [0, 1, 0], [-np.sin(angle), 0, np.cos(angle)]])
        rotated_xyz = np.dot(self.xyz, rot_mat.T)
        self.xyz = rotated_xyz
        self.set_new_coords_to_atoms()
        return self

    def translation_x(self, distance):
        """
        Translates the atom's position along the x-axis by a specified distance.

        This method updates the atom's x-coordinate by adding the given distance
        while keeping the y and z coordinates unchanged.

        :param distance: The distance to translate along the x-axis (float).
        :modify self: Updates the atom's position by shifting along the x-axis.
        :return: The updated object instance with the new coordinates.
        """
        translated_xyz = self.xyz + np.array([distance, 0, 0])
        self.xyz = translated_xyz
        self.set_new_coords_to_atoms()
        return self

    def translation_y(self, distance):
        """
        similar to translation_x

        :param distance: The distance to translate along the y-axis (float).
        :modify self: Updates the atom's position by shifting along the y-axis.
        :return: The updated object instance with the new coordinates.
        """
        translated_xyz = self.xyz + np.array([0, distance, 0])
        self.xyz = translated_xyz
        self.set_new_coords_to_atoms()
        return self

    def translation_z(self, distance):
        """
         similar to translation_x

        :param distance: The distance to translate along the z-axis (float).
        :modify self: Updates the atom's position by shifting along the z-axis.
        :return: The updated object instance with the new coordinates.
        """
        translated_xyz = self.xyz + np.array([0, 0, distance])
        self.xyz = translated_xyz
        self.set_new_coords_to_atoms()
        return self

    def set_new_coords_to_atoms(self):
        """
        Updates the coordinates of all atoms based on the current positions stored in `xyz`.

        This method iterates through each atom and assigns it the corresponding coordinates
        from the `xyz` list, updating each atom's position accordingly.

        :modify self: Updates the position of each atom in the system using the coordinates
                      stored in the `xyz` attribute.
        :return: None
        """
        # print("from molecule.set_new_coords_to_atoms() ,,,,,,,")
        # print([i.number for i in self.atoms], self.xyz)
        for atom, coords in zip(self.atoms, self.xyz):
            atom.update_coordinates(*coords)


    def add_atom(self, atom):
        """ add an atom to the molecule and update the center of mass
        :param atom: Atom object to be added to the molecule.
        :modify self: Adds the atom to the molecule's atom list and recalculates the center of mass.
        to update the parameters x,y,z,center_of_mass and xyz
        :return: None"""
        self.atoms.append(atom)
        self.xyz = np.array([atom.get_coords() for atom in self.atoms])
        self.cal_center_of_mass()

    def number_of_atoms(self):
        """ returns the number of atoms in the molecule
        :return: int: Number of atoms in the molecule."""
        return len(self.atoms)

    def cal_center_of_mass(self):
        """ calculates the center of mass of the molecule
        :return: list: A list containing the x, y, z coordinates of the center of mass."""
        gp= center_of_mass(self.atoms)
        self.x = gp[0]
        self.y = gp[1]
        self.z = gp[2]
        return gp

    def to_str(self):
        """ returns the string representation of the molecule in xyz format
        :return: str: A string containing the number of atoms, a blank line, and the
                      xyz coordinates of each atom in the molecule."""
        str = ""
        for atom in self.atoms:
            str += atom.to_str() + "\n"
        print(str)
        return str[:-1]

    def __str__(self):
        """ returns the string representation of the molecule in xyz format
        :return: str: A string containing the number of atoms, a blank line, and the
                      xyz coordinates of each atom in the molecule."""
        return self.to_str()

    def get_coords(self):
        """ returns the coordinates of the molecule's center of mass"""
        return self.center_of_mass

    def update_coordinates(self, x, y, z):
        """
        Updates the coordinates of the atoms based on a new center of mass(COM) point.

        This method calculates the displacement between the current COM point
        and the new specified COM. It then translates the molecule's
        coordinates accordingly along each axis and updates the COM.

        :param x: New x-coordinate of the COM (float).
        :param y: New y-coordinate of the COM (float).
        :param z: New z-coordinate of the COM (float).
        :modify self: Updates the molecule's position by applying the calculated
                      translation and recalculates the COM.

        :return: None
        """

        new_center_of_mass = [x, y, z]
        change_in_center_of_mass = np.array(new_center_of_mass) - np.array(self.center_of_mass)
        self.translation_x(change_in_center_of_mass[0])
        self.translation_y(change_in_center_of_mass[1])
        self.translation_z(change_in_center_of_mass[2])
        self.center_of_mass = self.cal_center_of_mass()


    def relative_coordination_matrix(self):
        """ return the coordination matrix of the molecule relative to its center of mass"""
        xyz_matrix = np.array([atom.get_coords() for atom in self.atoms])
        relative_atom_coords = xyz_matrix - center_of_mass(self.atoms)
        return relative_atom_coords

    def change_center_of_mass(self, center_of_mass):
        """ change the molecule coordinates without the bond distances and angles to a new center of mass
        :param center_of_mass: list: A list containing the new x, y, z coordinates of the center of mass."""

        self.xyz = self.relative_coordination_matrix() + center_of_mass
        self.cal_center_of_mass()
        self.set_new_coords_to_atoms()




    def distance_between(self, other):
        """ returns the distance between two molecules based on their center of mass
         :param other: Molecule object to calculate the distance to.
         :return: float: The Euclidean distance between the centers of mass of the two molecules."""
        diff_x = pow(self.x - other.x, 2)
        diff_y = pow(self.y - other.y, 2)
        diff_z = pow(self.z - other.z, 2)
        return pow(diff_z + diff_x + diff_y, 0.5)

    def unit_position_vector(self):
        """
        returns the unit vector of the molecule based on its center of mass
        :return: list of float: A list containing the x, y, z components of the unit position vector.
        """
        magnitude = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
        return [self.x / magnitude, self.y / magnitude, self.z / magnitude]

    def distance_from_origin(self):
        """ returns the distance of the molecule from the origin based on its center of mass
        :return: float: The Euclidean distance from the origin (0,0,0) to the center of mass of the molecule."""
        diff_x = pow(self.x, 2)
        diff_y = pow(self.y, 2)
        diff_z = pow(self.z, 2)
        return pow(diff_z + diff_x + diff_y, 0.5)

    def calculate_RMSD(self):
        """ center of mass is used as the reference point to avoid the bias
        returns the root mean square deviation (RMSD) of the molecule based on its atoms' distances from the center of mass
        :return: float: The RMSD value calculated from the distances of each atom to the center of mass."""
        sum_of_distances_square = 0
        for atom in self.atoms:
            sum_of_distances_square += atom.distance_from_center_of_mass(self.center_of_mass) ** 2

        return (sum_of_distances_square/len(self.atoms))**0.5

    def reorient_molecule_to_start(self):
        """ reorient the molecule to its initial orientation and recalculate the center of mass"""
        for atom in self.atoms:
            atom.reorient_atom_to_start()
        self.cal_center_of_mass()

