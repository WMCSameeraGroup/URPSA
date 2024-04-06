import sys
from LogReader.log_file_manager import LogFileManager
from calculations.calculation_manager import run_calculation
from inputFileGeneration.coordinates import coordinate_generation, string_of_atoms_coordinates
from inputFileGeneration.input_file_writer import input_file_config
from LogReader.log_file_reader import get_input_files_list, find_corresponding_output_file
from inputfile import InputFile
from calculations.Is_too_close import is_not_highly_repulsive

file_path = sys.argv[1]

system = InputFile(file_path)  # read input file and understand data

# todo: implement rotation using molecule package

coordinates = coordinate_generation(system.atom_list, system.step_count, system.step_size)  # coordinate generation

for number, coordinate in enumerate(coordinates):
    coordinate_string = string_of_atoms_coordinates(system.atom_list, coordinate)
    input_file_config(number, coordinate_string, system)

all_input_files = get_input_files_list()
output_file_list = []

for file in all_input_files:
    if is_not_highly_repulsive(file, len(system.origin_atoms)):
        if run_calculation(file) != 0:  # something went wrong  thus no log file is produced
            continue
        print(find_corresponding_output_file(file), file)
        log = LogFileManager(find_corresponding_output_file(file))
        output_file_list.append(log)
    else:
        print(f"{file} is too repulsive to calculate")
        break  # stop if repulsion was encountered

for obj in output_file_list:
    print(obj.scf_done)

import matplotlib.pyplot as plt


def plot_the_graph(outputFiles):
    data = [float(f.scf_done[0]) for f in outputFiles if f.scf_done != "could not found"][:-1]
    plt.plot(data)
    plt.savefig("output.jpg")


plot_the_graph(output_file_list)
