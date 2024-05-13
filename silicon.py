from matplotlib import pyplot as plt

from LogReader.log_file_manager import LogFileManager
from LogReader.log_file_reader import get_input_files_list, find_corresponding_output_file
from atoms.atoms import Atom
from settings import input_file_directory
from calculations.Is_too_close import is_not_highly_repulsive
from calculations.calculation_manager import run_calculation
from calculations.random_spherical_coords_generator import random_spherical_coordinates_generator
from inputFileGeneration.coordinates import string_of_atoms_coordinates
from inputFileGeneration.input_file_writer import input_file_config
from molecule.molecule import Molecule
from inputFileGeneration.spherical_grid_coordinates import spherical_gird_coordinate_generation
from system import System

"""
create silicon atoms in the coordination sphere of atoms
"""


def plot_the_graph(outputFiles, file_name="output.jpg"):
    data = [float(f.scf_done[0]) for f in outputFiles if f.scf_done != "could not found"][:-1]
    plt.plot(data)
    plt.ylabel("Energy/AU")
    plt.xlabel("Step")
    plt.savefig(input_file_directory + "/" + file_name)


def run(num_of_silicon_atoms=3, radius=10):
    silicon_atoms = []
    for n in range(num_of_silicon_atoms):
        silicon_atoms.append(Atom("Si", *random_spherical_coordinates_generator(radius)))

    silicon_cluster = Molecule(silicon_atoms)
    coordinates = spherical_gird_coordinate_generation(silicon_cluster, 7, 1)

    system = System(silicon_atoms, 0, 1)

    for number, coordinate in enumerate(coordinates):
        coordinate_string = string_of_atoms_coordinates(silicon_cluster.atoms, coordinate)
        print(coordinate_string)
        input_file_number = number
        input_file_config(input_file_number, coordinate_string, system)

    ####################################################################################

    all_input_files = get_input_files_list()
    output_file_list = []

    for file in all_input_files:

        if run_calculation(file) != 0:  # something went wrong  thus no log file is produced
            continue
        print(find_corresponding_output_file(file), file)
        log = LogFileManager(find_corresponding_output_file(file))
        output_file_list.append(log)

    for obj in output_file_list:
        print(obj.scf_done)
    plot_the_graph(output_file_list)




run()
