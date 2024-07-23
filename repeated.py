
import sys
from LogReader.log_file_manager import LogFileManager
from calculations.calculation_manager import run_calculation
from LogReader.log_file_reader import find_corresponding_output_file
from inputFileGeneration.spherical_grid_coordinates import spherical_gird_coordinate_generation
from inputfile import InputFile
from calculations.Is_too_close import is_not_highly_repulsive_spherically


from outputFiileWriter.output_writer import OutputWriter
from settings import input_file_directory
from utils.transferFiles import move_files_to_timestamped_folder, move_files_to_project_folder
from system.system import System
from outputFiileWriter.setup import Setup


import matplotlib.pyplot as plt


def plot_the_graph(outputFiles, file_name="output.jpg"):
    data = [float(f.scf_done) for f in outputFiles if f.scf_done != "could not found"][::-1]
    plt.plot(data)
    plt.ylabel("Energy/AU")
    plt.xlabel("Step")
    plt.savefig(input_file_directory + "/" + file_name)
    plt.clf()


def plot_scatter(outputFiles, file_name="scatter.jpg"):
    x_coords = []
    y_coords = []
    for index, j in enumerate(outputFiles):
        if j.is_converged == 0:
            x_coords.append(index)
            y_coords.append(float(j.scf_done))
            print(index,j.scf_done)

    plt.scatter(x_coords,y_coords)
    plt.ylabel("Energy/AU")
    plt.xlabel("Step")
    plt.savefig(input_file_directory + "/" + file_name)
    plt.clf()


try:
    file_path = sys.argv[1]
except:
    print("a input file is not provided")
    sys.exit()

controls = InputFile(file_path)  # read input file and understand data
system = System(controls.charge, controls.multiplicity, controls.method, controls.cores)
system.add_list_of_molecules(controls.list_of_molecules)
setup = Setup(controls.project_name)

for i in range(controls.n_iterations):
    system.re_orient_molecules(controls)
    system.random_rotate_molecules()
    print(i)
    output_file_list =[]
    #################################################################################
    for iteration in range(controls.step_count):
        spherical_gird_coordinate_generation(system.molecules, controls.step_count, controls.step_size)
        inputFile = system.generate_input_file(iteration)
        if is_not_highly_repulsive_spherically(system,controls.stop_distance_factor):
            # if run_calculation(inputFile) != 0:  # something went wrong  thus no log file is produced
            #     continue
            success = run_calculation(inputFile)
            try:
                log = LogFileManager(find_corresponding_output_file(inputFile))
                log.is_converged=success
            except:
                continue
            output_file_list.append(log)

            system.set_scf_done(log.scf_done)
            if controls.update_with_optimized_coordinates == "True" and success == 0:
                print("update_with_optimized_coordinates")
                system.set_moleculer_coordinates(log.opt_coords)

            OutputWriter().write_xyz_file(system,log.opt_coords)
        else:
            print(f"{inputFile} is too repulsive to calculate")
            break  # stop if repulsion was encountered

    plot_the_graph(output_file_list)
    plot_scatter(output_file_list)

    new_name = controls.project_name + "/" + setup.get_next_folder_name()
    move_files_to_project_folder(new_name)

# need to add another exit condition same position twice then exit
# some times it replaces the atom and stays there

####################################################################################






