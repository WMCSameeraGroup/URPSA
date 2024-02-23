MASS = {"H":1,"O":16}
VANDER_WALLS ={"H": 1.20, "O": 1.52}
class Atom:

    def __init__(self,symbol,x,y,z):
        self.symbol = symbol
        self.mass = MASS[symbol]
        self.v_radius = VANDER_WALLS[symbol]
        self.x =float(x)
        self.y =float(y)
        self.z =float(z)

    def __str__(self):
        return f"{self.symbol} {self.x} {self.y} {self.z}"

    def get_coords(self):
        return [self.x, self.y, self.z]

    def update_coordinates(self,x,y,z):
        self.x =float(x)
        self.y =float(y)
        self.z =float(z)

    def distance_between(self,other):
        diff_x = pow(self.x, 2)-pow(other.x, 2)
        diff_y = pow(self.y, 2)-pow(other.y, 2)
        diff_z = pow(self.z, 2)-pow(other.z, 2)
        return pow(diff_z+diff_x+diff_y,0.5)


