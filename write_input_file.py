output_dir = 'inputFiles'

import os
def write_input_file(file_name,data):
    # just write to the file
    if output_dir not in os.listdir():
        os.mkdir(output_dir)

    with open(output_dir+'/'+file_name,'w') as input_file:
        input_file.write(data)
