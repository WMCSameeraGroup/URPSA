
import sys
from LogReader.log_file_manager import LogFileManager
from calculations.calculation_manager import run_calculation
from LogReader.log_file_reader import find_corresponding_output_file
from inputFileGeneration.spherical_grid_coordinates import spherical_gird_coordinate_generation
from inputfile import InputFile
from calculations.Is_too_close import is_not_highly_repulsive_spherically


from outputFiileWriter.output_writer import OutputWriter
from settings import input_file_directory
from utils.transferFiles import move_files_to_timestamped_folder
from system.system import System

try:
    file_path = sys.argv[1]
except:
    print("a input file is not provided")
    sys.exit()

controls = InputFile(file_path)  # read input file and understand data
system = System(controls.charge, controls.multiplicity)
system.add_list_of_molecules(controls.list_of_molecules)

# transfer previous file to archives folder
move_files_to_timestamped_folder()
output_file_list =[]
#################################################################################
for iteration in range(controls.step_count):
    spherical_gird_coordinate_generation(system.molecules, controls.step_count, controls.step_size)
    inputFile = system.generate_input_file(iteration)
    if is_not_highly_repulsive_spherically(inputFile):
        # if run_calculation(inputFile) != 0:  # something went wrong  thus no log file is produced
        #     continue
        run_calculation(inputFile)
        try:
            log = LogFileManager(find_corresponding_output_file(inputFile))
        except:
            continue
        output_file_list.append(log)

        system.set_scf_done(log.scf_done)
        if controls.update_with_optimized_coordinates:
            system.set_moleculer_coordinates(log.opt_coords)

        OutputWriter().write_xyz_file(system)
    else:
        print(f"{inputFile} is too repulsive to calculate")
        break  # stop if repulsion was encountered

####################################################################################
for obj in output_file_list:
    print(obj.scf_done)


import matplotlib.pyplot as plt


def plot_the_graph(outputFiles, file_name="output.jpg"):
    data = [float(f.scf_done) for f in outputFiles if f.scf_done != "could not found"][::-1]
    plt.plot(data)
    plt.ylabel("Energy/AU")
    plt.xlabel("Step")
    plt.savefig(input_file_directory + "/" + file_name)


plot_the_graph(output_file_list)
