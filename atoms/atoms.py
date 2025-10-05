
from .constants import MASS,COVALENT_RADIUS

class Atom:

    def __init__(self, symbol, x, y, z, number, fixed="False"):
        """
        Initializes an atom object with specific properties.

        This constructor sets the atom's element symbol, coordinates, atomic number,
        mass, covalent radius, and whether the atom is fixed or not.

        :param symbol: The chemical symbol of the atom (string).
        :param x: The x-coordinate of the atom (float).
        :param y: The y-coordinate of the atom (float).
        :param z: The z-coordinate of the atom (float).
        :param number: The atomic number of the atom (integer).
        :param fixed: Specifies whether the atom is fixed in place ("fixed" or "False"). Default is "False" (string).
        """

        self.number = number
        self.symbol = symbol
        self.mass = MASS[symbol]
        self.c_radius = COVALENT_RADIUS[symbol]
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.starting_positions =[float(x),float(y),float(z) ]
        self.is_fixed = fixed.lower() == "fixed" if isinstance(fixed, str) else bool(fixed)

    def __str__(self):
        """Returns a string representation of the atom."""
        if self.is_fixed:
            return f"{self.symbol} -1 {self.x} {self.y} {self.z}"
        return f"{self.symbol} {self.x} {self.y} {self.z}"

    def to_str(self):
        """Returns a string representation of the atom."""
        return f"{self.symbol} {self.x} {self.y} {self.z}"
    def get_coords(self):
        """
        Returns the current coordinates of the atom as a list.
        :rtype: list
        :example: [1.0, 2.0, 3.0]
        :return: A list containing the x, y, and z coordinates of the atom.
        """
        return [self.x, self.y, self.z]

    def update_coordinates(self, x, y, z):
        """
        Updates the atom's position to the specified coordinates.

        This method sets the atom's x, y, and z coordinates to the new values provided.

        :param x: The new x-coordinate of the atom (float).
        :param y: The new y-coordinate of the atom (float).
        :param z: The new z-coordinate of the atom (float).
        :modify self: Updates the atom's position with the new coordinates.
        :return: None
        """

        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def distance_between(self, other):
        """
        Calculates the Euclidean distance between this atom and another atom.
        :param other: Another Atom object to calculate the distance to.
        :return: The Euclidean distance between the two atoms.
        :rtype: float
        :example: 1.732
        """
        diff_x = pow(self.x - other.x, 2)
        diff_y = pow(self.y - other.y, 2)
        diff_z = pow(self.z - other.z, 2)
        return pow(diff_z+diff_x+diff_y, 0.5)

    def distance_from_center_of_mass(self,COM):
        """
        Calculates the Euclidean distance from the atom to a given center of mass (COM).
        :param COM:list or tuple
            A list or tuple representing the x, y, and z coordinates of the center of mass.
        :rtype: float
        :example: 2.236
        :return: distance from the atom to the center of mass.
        """
        diff_x = pow(self.x - COM[0], 2)
        diff_y = pow(self.y - COM[1], 2)
        diff_z = pow(self.z - COM[2], 2)
        return pow(diff_z + diff_x + diff_y, 0.5)

    def unit_position_vector(self):
        """
        Calculates the unit position vector of the atom based on its current coordinates.
        :rtype: list
        :example: [0.267, 0.534, 0.801]
        :return:
        """
        magnitude = (self.x**2 + self.y**2 + self.z**2)**0.5
        return [self.x/magnitude, self.y/magnitude, self.z/magnitude]

    def distance_from_origin(self):
        """
        Calculates the Euclidean distance from the atom to the origin (0, 0, 0).
        :return: distance from the atom to the origin.
        :rtype: float
        :example: 3.605
        """
        diff_x = pow(self.x, 2)
        diff_y = pow(self.y, 2)
        diff_z = pow(self.z, 2)
        return pow(diff_z+diff_x+diff_y, 0.5)


    def reorient_atom_to_start(self):
        """ Resets the atom's coordinates to its original starting positions.
        :modify self: Updates the atom's coordinates to the starting positions.
        :return: None
        """
        self.x = self.starting_positions[0]
        self.y = self.starting_positions[1]
        self.z = self.starting_positions[2]

