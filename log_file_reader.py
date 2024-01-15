""" go to log files directory starts reading them and log files form log files folder then
 grab the data required.
 """
# todo: make a input and output file manager class/ run this in another thread to read and plot data while same
#  calculations are done
from settings import input_file_directory, output_file_directory
import os


def inputFileValidator(file_name):
    return True


def get_input_files_list():
    input_files_list = os.listdir(input_file_directory)
    input_files_list = [file for file in input_files_list if inputFileValidator(file)]
    return input_files_list
