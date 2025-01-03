import sys
from operator import index

from LogReader.log_file_manager import LogFileManager
from calculations.calculation_manager import run_calculation
from LogReader.log_file_reader import find_corresponding_output_file
from inputFileGeneration.spherical_grid_coordinates import push_fragments_to_center
from setup.inputfile import InputFile
from calculations.Is_too_close import is_not_highly_repulsive_spherically

from outputFiileWriter.output_writer import OutputWriter
from utils.ploting import plot_scatter
from system.system import System
from outputFiileWriter.setup import Setup
from productCatogarization.catogarize_products import products_writer,get_new_molecules
from productCatogarization.collection_of_products import productsManager

try:
    file_path = sys.argv[1]
except IndexError:
    print("a valid input file is not provided")
    sys.exit()

controls = InputFile(file_path)  # read input file and understand data
system = System(controls)
setup = Setup(controls.project_name)


products_collection = productsManager(controls.project_name+"/")
for i in range(controls.n_iterations):
    system.remove_all_molecules()
    controls.set_molecule_list()
    system.add_list_of_molecules(controls.list_of_molecules)
    system.re_orient_molecules(controls)
    system.random_rotate_molecules()
    output_file_list = []
    print(i)

    dir_of_files = controls.project_name + "/" + setup.get_next_folder_name()
    is_all_calculations_converged = True
    #################################################################################
    for iteration in range(controls.step_count):

        push_fragments_to_center(system.molecules, controls.step_size)
        inputFile = system.generate_input_file(iteration, dir_of_files)
        if is_not_highly_repulsive_spherically(system, controls.stop_distance_factor):
            success = run_calculation(inputFile, dir_of_files)
            print(success)

            try:
                log = LogFileManager(find_corresponding_output_file(inputFile), dir_of_files)
                log.is_converged = success

            except Exception as e:
                print(e)
                continue
            output_file_list.append(log)

            system.set_scf_done(log.scf_done)

            OutputWriter(dir_of_files).write_xyz_file(system, log.opt_coords)

            if system.get_energy_gap(output_file_list[0].scf_done,log.scf_done) > controls.cutoff_energy_gap:
                is_all_calculations_converged = False
                print("Energy gap between products and reactants is more than the cutoff energy gap \n ignoring the path due to high energy gap :{}".format(system.get_energy_gap(output_file_list[0].scf_done,log.scf_done)))
                if controls.energy_surpass_options == "optimize":
                    system.stress_release.append(iteration+1)
                elif controls.energy_surpass_options == "exit":
                    break



            if success != 0: # print the error
                print(log.last_lines())
                is_all_calculations_converged = False
                if controls.convergence_error == "exit":
                    break

            if controls.update_with_optimized_coordinates == "True" and success == 0:
                print("update_with_optimized_coordinates")
                system.set_moleculer_coordinates(log.opt_coords)
                if controls.dynamic_fragment_replacement == "True":
                    new_molecules = get_new_molecules(system.set_list_of_atom_symbols(), log)
                    system.replace_molecules(new_molecules)
                    if len(new_molecules) == 1:
                        # optimize the last observed particle
                        if controls.optimize_the_final_particle == "True":
                            print("final structure is optimizing.....")
                            try:
                                optFile = system.generate_input_file(-1, dir_of_files)
                                val=run_calculation(optFile, dir_of_files)
                                final_log = LogFileManager(find_corresponding_output_file(optFile), dir_of_files)
                                final_log.is_converged = val
                                output_file_list.append(final_log)
                                system.set_scf_done(final_log.scf_done)
                                OutputWriter(dir_of_files).write_xyz_file(system, final_log.opt_coords)
                                print("final structure is optimized")
                            except Exception as e:
                                print(f"An error occur while optimizing the final fragments :\n{e} ")

                        break





        else:
            print(f"{inputFile} is too repulsive to calculate")
            break  # stop if repulsion was encountered
            #todo: possibly a constraint less optimization for relaxation.

    plot_scatter(output_file_list, dir_of_files)

    if is_all_calculations_converged:
        # find products and label them
        products = products_writer(dir_of_files)
        products_molecules=products.get_products_list(system.set_list_of_atom_symbols(), output_file_list)

        products_collection.write_product(i+1,products_molecules)
        print("number of similar products found")
        print(products_collection.check_number_of_times_same_products_were_observed(i,products_molecules))
    else:
        # todo: delete the file or do something
        pass

    # todo:if n times same molecules were found exit the loop

####################################################################################
