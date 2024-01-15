from settings import input_file_directory

import os
def write_input_file(file_name,data):
    # just write to the file
    if input_file_directory not in os.listdir():
        os.mkdir(input_file_directory)

    with open(input_file_directory+'/'+file_name,'w') as input_file:
        input_file.write(data)
