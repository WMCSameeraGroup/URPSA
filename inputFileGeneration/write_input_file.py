


import os


def generate_input_file(file_name,input_file_directory, data):
    """Generate an input file with the given data in the specified directory.
    :param file_name: Name of the input file to be created.
    :param input_file_directory: Directory where the input file will be saved.
    :param data: Content to be written into the input file.
    :return: None"""

    if input_file_directory not in os.listdir():
        try:
            os.mkdir(input_file_directory)
        except FileExistsError:
            pass

    with open(input_file_directory+'/'+file_name, 'w') as input_file:
        input_file.write(data)

