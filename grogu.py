import sys

from LogReader.log_file_manager import LogFileManager
from calculations.calculation_manager import run_calculation
from calculations.gravitypoint import gravity_point
from inputFileGeneration.coordinates import coordinate_generation,string_of_atoms_coordinates
from atoms.atoms import Atom
from inputFileGeneration.input_file_writer import input_file_config
from LogReader.log_file_reader import get_input_files_list,find_corresponding_output_file

file_path = sys.argv[1]

variable_parameters =[]
file_data=""
atom_list = []
# todo: charge and multiplicity from the input file

try:
    with open(file_path,'r') as file:
        file_data=file.read()
except:
    print(file_path +" not found")

for line in file_data.split("\n\n")[0].split("\n"):
    line_data=line.split()
    atom_list.append(Atom(*line_data))

step_size = float(file_data.split("\n\n")[1].split()[0])
step_count = int(float(file_data.split("\n\n")[1].split()[1]))


#print(gravity_point(atom_list))

coordinates=coordinate_generation(atom_list,step_count,step_size)

for number, coordinate in enumerate(coordinates):
    coordinate_string = string_of_atoms_coordinates(atom_list,coordinate)
    input_file_config(number,coordinate_string)



input_files = get_input_files_list()

output_file_list =[]

for file in input_files:
    run_calculation(file)
    print(find_corresponding_output_file(file), file)
    log = LogFileManager(find_corresponding_output_file(file))
    output_file_list.append(log)


for obj in output_file_list:
    print(obj.scf_done)







