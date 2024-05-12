from atoms.atoms import Atom
from calculations.random_spherical_coords_generator import random_spherical_coordinates_generator
from inputFileGeneration.coordinates import string_of_atoms_coordinates
from inputFileGeneration.input_file_writer import input_file_config
from molecule.molecule import Molecule
from inputFileGeneration.spherical_grid_coordinates import spherical_gird_coordinate_generation
"""
create silicon atoms in the coordination sphere atoms
"""

number_of_silicon_atoms = 3
radius = 10

silicon_atoms = []
for n in range(number_of_silicon_atoms):
    silicon_atoms.append(Atom("Si", *random_spherical_coordinates_generator(10)))

silicon_cluster = Molecule(silicon_atoms)
coordinates = spherical_gird_coordinate_generation(silicon_cluster, 3, 1)

for number, coordinate in enumerate(coordinates):
    coordinate_string = string_of_atoms_coordinates(silicon_cluster.atoms, coordinate)
    # input_file_number = number
    # input_file_config(input_file_number, coordinate_string, silicon_cluster)
