""" go to log files directory starts reading them and log files form log files folder then
 grab the data required.
 """
# todo: make a input and output file manager class/ run this in another thread to read and plot data while same
#  calculations are done
from settings import input_file_directory, output_file_directory
import os, re


def input_file_validator(file_name):
    return True


def get_input_files_list():
    input_files_list = os.listdir(input_file_directory)
    input_files_list = [file for file in input_files_list if input_file_validator(file)]
    return order_input_files(input_files_list)


def order_input_files(input_files):
    def extract_number(file):
        # Use regular expression to extract the number from the name
        match = re.search(r'\d+', file)
        return int(match.group()) if match else 0

    # Sort the names based on the extracted numbers
    sorted_names = sorted(input_files, key=extract_number)

    return sorted_names


def find_corresponding_output_file(inputfile):
    output_files_list = os.listdir(output_file_directory)
    if inputfile + ".LOG" in output_files_list:
        return inputfile + ".LOG"
