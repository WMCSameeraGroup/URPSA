from inputFileGeneration.input_file_writer import generate_input_files
from settings import step_size, step_count
from LogReader.log_file_reader import get_input_files_list,find_corresponding_output_file
from calculations.calculation_manager import run_calculation
from LogReader.log_file_manager import LogFileManager

"""generate input files"""
generate_input_files(step_size, step_count)

""" read input and do calculations and get data one by one """

input_files = get_input_files_list()

output_file_list =[]

for file in input_files:
    run_calculation(file)

    log = LogFileManager(find_corresponding_output_file(file))
    output_file_list.append(log)



    # todo : write a file to recored data