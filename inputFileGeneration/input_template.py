from settings import input_file_directory as inp_dir


def get_input_template(number, system, method="wb97xd/aug-cc-pvtz"): # Todo: a way to specify method
    # gonna replace title value
     return """%chk={3}/test{0}.chk
# {4}

Title{0}
 
{1} {2}	\n""".format(number,system.charge,system.multiplicity,inp_dir,method)


if __name__ =="__main__":
    print(get_input_template(1))