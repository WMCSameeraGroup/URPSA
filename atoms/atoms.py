from .constants import MASS,VANDER_WALLS

class Atom:

    def __init__(self,symbol,x,y,z):
        self.symbol = symbol
        self.mass = MASS[symbol]
        self.v_radius = VANDER_WALLS[symbol]
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __str__(self):
        return f"{self.symbol} {self.x} {self.y} {self.z}"

    def get_coords(self):
        return [self.x, self.y, self.z]

    def update_coordinates(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def distance_between(self, other):
        diff_x = pow(self.x - other.x, 2)
        diff_y = pow(self.y - other.y, 2)
        diff_z = pow(self.z - other.z, 2)
        return pow(diff_z+diff_x+diff_y, 0.5)

    def unit_position_vector(self):
        magnitude = (self.x**2 + self.y**2 + self.z**2)**0.5
        return [self.x/magnitude, self.y/magnitude, self.z/magnitude]

