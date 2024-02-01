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
    print(find_corresponding_output_file(file), file)
    log = LogFileManager(find_corresponding_output_file(file))
    output_file_list.append(log)


for obj in output_file_list:
    print(obj.scf_done)

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.collections import EventCollection

def plot_the_graph(outputFiles):
    plt.plot([file.scf_done for file in outputFiles][:-1])
    plt.show()