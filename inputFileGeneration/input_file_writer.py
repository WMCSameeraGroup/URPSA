from inputFileGeneration.input_template import get_input_template
from inputFileGeneration.write_input_file import generate_input_file



def setup_input_file(coordinate, template, system):
    """ sets up the input file string
    :param coordinate: string
        xyz coordinates of the system
    :param template: string
        input file template
    :param system: System
        system object containing molecules and other properties charge, multiplicity etc
    :return: string to be written in the input file
    """
    return template + coordinate + system.molecules[0].to_str() + "\n\n\n\n"


def file_name_generator(number,input_file_name="step"):
    """ generates the file name for the input file
    :param number: int
        step number
    :param input_file_name: string
        base name for the input file
    :return: string
        file name for the input file
    """
    return input_file_name + str(number) + ".com"


def input_file_config(number, coordinate_string, system):
    """ generates the input file for the given step number and coordinate string
    :param number: int step number
    :param coordinate_string: string
        xyz coordinates of the system
    :param system: System
        system object containing molecules and other properties charge, multiplicity etc
    :return: None
    """
    template = get_input_template(number, system)
    file_name = file_name_generator(number)
    string_to_be_written = setup_input_file(coordinate_string, template, system)
    generate_input_file(file_name, string_to_be_written)

