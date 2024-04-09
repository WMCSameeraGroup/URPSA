from inputFileGeneration.input_template import get_input_template
from inputFileGeneration.write_input_file import generate_input_file
from settings import input_file_name


def setup_input_file(coordinate, template, system):
    return template + coordinate + system.origin_molecule + "\n\n\n\n"
    # "H -0.89 -2.00 -0.89\nH -0.89 -2.00 0.89\nO -0.11 -1.00 -0.11"+'\n\n\n'


def file_name_generator(number):
    # todo : change this thing not to overight everything
    return input_file_name + str(number) + ".com"


def input_file_config(number, coordinate_string, system):
    """new file generator """
    template = get_input_template(number, system)
    file_name = file_name_generator(number)
    string_to_be_written = setup_input_file(coordinate_string, template, system)
    generate_input_file(file_name, string_to_be_written)
