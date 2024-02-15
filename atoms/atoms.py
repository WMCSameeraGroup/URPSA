MASS = {"H":1,"O":16}
class Atom:

    def __init__(self,symbol,x,y,z):
        self.symbol = symbol
        self.mass = MASS[symbol]
        self.x =float(x)
        self.y =float(y)
        self.z =float(z)

    def __str__(self):
        return f"{self.symbol} {self.x} {self.y} {self.z}"

    def get_coords(self):
        return [self.x, self.y, self.z]

