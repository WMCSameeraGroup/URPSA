from matplotlib import pyplot as plt
import sys
from LogReader.log_file_manager import LogFileManager
from LogReader.log_file_reader import get_input_files_list, find_corresponding_output_file

from inputfile import InputFile
from settings import input_file_directory
from calculations.Is_too_close import is_not_highly_repulsive_spherically
from calculations.calculation_manager import run_calculation

from inputFileGeneration.coordinates import string_of_atoms_coordinates
from inputFileGeneration.input_file_writer import input_file_config
from molecule.molecule import Molecule
from inputFileGeneration.spherical_grid_coordinates import spherical_gird_coordinate_generation

from utils.transferFiles import move_files_to_timestamped_folder
from outputFiileWriter.output_writer import OutputWriter

"""
create silicon atoms in the coordination sphere of atoms
"""

try:
    file_path = sys.argv[1]
except:
    print("a input file is not provided")
    sys.exit()

system = InputFile(file_path)  # read input file and understand data


# todo: set multiplicity / use an inputfile
def plot_the_graph(outputFiles, file_name="output.jpg"):
    data = [float(f.scf_done[0]) for f in outputFiles if f.scf_done != "could not found"][::-1]
    plt.plot(data)
    plt.ylabel("Energy/AU")
    plt.xlabel("Step")
    plt.savefig(input_file_directory + "/" + file_name)


def run(system):
    # transfer previous file to archives folder
    move_files_to_timestamped_folder()

    cluster = Molecule(system.atom_list)
    coordinates = spherical_gird_coordinate_generation(cluster, system.step_count, system.step_size)

    for number, coordinate in enumerate(coordinates):
        coordinate_string = string_of_atoms_coordinates(cluster.atoms, coordinate)
        print(coordinate_string)
        input_file_number = number
        input_file_config(input_file_number, coordinate_string, system)

    ####################################################################################

    all_input_files = get_input_files_list()
    output_file_list = []

    for file in all_input_files:

        try:
            if is_not_highly_repulsive_spherically(file):
                run_calculation(file)
                print(find_corresponding_output_file(file), file)
                log = LogFileManager(find_corresponding_output_file(file))
                output_file_list.append(log)
                OutputWriter().write_output_file(log)
            else:
                print("highly repulsive")
        except Exception as e:
            print(e)
            print("error occurred")
            # todo: what to add in an exception
        # todo: write an output file
    for obj in output_file_list:
        print(obj.scf_done)
    plot_the_graph(output_file_list)


run(system)
