from input_template import get_input_template
from coordinates import generate_coordinates
from write_input_file import write_input_file


def setup_input_file(coordinate, template):
    return template + coordinate + '\n\n\n'


def file_name_generator(number):
    return "test" + str(number)


def input_file_configuration_and_writing(number, steps=10, s_size=1):
    # generate the input file for a given number
    coordinate = generate_coordinates(num_of_steps=steps, step_size=s_size)[number]
    template = get_input_template(number)

    string_to_be_written = setup_input_file(coordinate, template)
    file_name = file_name_generator(number)

    write_input_file(file_name, string_to_be_written)


""" this file is to write when a """


def generate_input_files(step_size, number_of_steps):
    for i in range(number_of_steps):
        input_file_configuration_and_writing(i, s_size=step_size, steps=number_of_steps)


generate_input_files(0.5, 31)
