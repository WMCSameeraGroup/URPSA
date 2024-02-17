from inputFileGeneration.input_template import get_input_template
from inputFileGeneration.coordinates import generate_coordinates
from inputFileGeneration.write_input_file import generate_input_file
from settings import input_file_name


def setup_input_file(coordinate, template):
    return template + coordinate + "H -0.89 -2.00 -0.89\nH -0.89 -2.00 0.89\nO -0.11 -1.00 -0.11"+'\n\n\n'


def file_name_generator(number):
    return input_file_name + str(number) + ".com"



def input_file_config(number,coordinate_string):
    """new file generator """
    template = get_input_template(number)
    file_name = file_name_generator(number)
    string_to_be_written = setup_input_file(coordinate_string, template)
    generate_input_file(file_name, string_to_be_written)

# redundant
def input_file_configuration_and_writing(number, steps=10, s_size=1):
    # generate the input file for a given number
    coordinate = generate_coordinates(num_of_steps=steps, step_size=s_size)[number]
    template = get_input_template(number)

    string_to_be_written = setup_input_file(coordinate, template)
    file_name = file_name_generator(number)

    generate_input_file(file_name, string_to_be_written)


""" this file is to write when a """

# redundant
def generate_input_files(step_size, number_of_steps):
    """ this is what you call to generate input files"""
    for i in range(number_of_steps):
        input_file_configuration_and_writing(i, s_size=step_size, steps=number_of_steps)


if __name__ == "__main__":
    generate_input_files(0.5, 31)
