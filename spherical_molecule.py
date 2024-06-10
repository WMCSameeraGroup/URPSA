import math
import sys
from LogReader.log_file_manager import LogFileManager
from calculations.calculation_manager import run_calculation
from inputFileGeneration.coordinates import coordinate_generation, string_of_atoms_coordinates
from inputFileGeneration.input_file_writer import input_file_config
from LogReader.log_file_reader import get_input_files_list, find_corresponding_output_file
from inputfile import InputFile
from calculations.Is_too_close import is_not_highly_repulsive

import random
from utils.transferFiles import move_files_to_timestamped_folder
from system.system import System
try:
    file_path = sys.argv[1]
except:
    print("a input file is not provided")
    sys.exit()

controls = InputFile(file_path)  # read input file and understand data
system = System(controls.charge,controls.multiplicity)
system.add_molecule(controls.origin_molecule)

# transfer previous file to archives folder
move_files_to_timestamped_folder()

#################################################################################
for iteration in range(controls.n_iter):
    # change orientations randomly using molecule module
    # loop can be used to generate files with different orientations

    molecule = controls.dynamic_molecule
    system.add_molecule(molecule)

    if controls.rotation_step:  # Check if 'rotation-step'
        rotation_step = controls.rotation_step * controls.n_iter
        print(rotation_step)
        molecule.rotation_xy(rotation_step[0]).rotation_yz(rotation_step[1]).rotation_xz(rotation_step[2])

    elif controls.rotation_random:
        molecule.rotation_xy(random.uniform(0, math.pi)).rotation_yz(random.uniform(0, math.pi)).rotation_xz(
            random.uniform(0, math.pi))

    coordinates = coordinate_generation(molecule.atoms, controls.step_count, controls.step_size)  # coordinate generation

    for number, coordinate in enumerate(coordinates):
        coordinate_string = string_of_atoms_coordinates(system.molecules[1].atoms, coordinate)
        input_file_number = iteration * controls.step_count + number
        input_file_config(input_file_number, coordinate_string, system)

####################################################################################
all_input_files = get_input_files_list()
output_file_list = []

for i in range(controls.n_iter):
    for file in all_input_files[i * controls.step_count: (1 + i) * controls.step_count]:
        if is_not_highly_repulsive(file, system.molecules[0].number_of_atoms()+1):
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
    plt.ylabel("Energy/AU")
    plt.xlabel("Step")
    plt.savefig("output.jpg")


plot_the_graph(output_file_list)