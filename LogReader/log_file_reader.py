
""" go to log files directory starts reading them and log files from log files folder then
 grab the data required.
 """

import os, re


def input_file_validator(file_name):
    """Validate if the file is a Gaussian input file based on its extension.
    Args
        file_name (str): The name of the file to be validated.
    :return bool: True if the file is a valid Gaussian input file, False otherwise."""

    return file_name[-3:] == 'com'


def get_input_files_list(input_file_directory):
    """
    Get a sorted list of valid Gaussian input files from the specified directory.

    Args:
        input_file_directory (str): Path to the directory containing input files.

    Returns:
        list: Sorted list of valid Gaussian input file names.
    """
    input_files_list = os.listdir(input_file_directory)
    input_files_list = [file for file in input_files_list if input_file_validator(file)]
    return order_input_files(input_files_list)


def order_input_files(input_files):
    """
    Sorts a list of input file names based on the first number found in each name.

    Args:
        input_files (list): List of input file names.

    Returns:
        list: Sorted list of input file names by extracted number.
    """
    def extract_number(file):
        # Use regular expression to extract the number from the name
        match = re.search(r'\d+', file)
        return int(match.group()) if match else 0

    # Sort the names based on the extracted numbers
    sorted_names = sorted(input_files, key=extract_number)

    return sorted_names


def find_corresponding_output_file(inputfile):
    """
    Given a Gaussian input file name, return the corresponding output log file name.

    Args:
        inputfile (str): The name of the input file.

    Returns:
        str: The corresponding output log file name.
    """
    return inputfile[:-3] + "log"





