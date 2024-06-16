from settings import input_file_directory as inp_dir



def get_input_template(number, system, method,num_of_cores):
    # gonna replace title value
    return """%NProcShared={5}
%chk={3}/test{0}.chk
# {4}

Title{0}
 
{1} {2}	\n""".format(number, system.charge, system.multiplicity, inp_dir, method,num_of_cores)


