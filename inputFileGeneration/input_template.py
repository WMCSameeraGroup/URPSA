from settings import input_file_directory as inp_dir
from settings import method


def get_input_template(number, system, calc_method=method):
    # gonna replace title value
    return """%chk={3}/test{0}.chk
# {4}

Title{0}
 
{1} {2}	\n""".format(number, system.charge, system.multiplicity, inp_dir, calc_method)


if __name__ == "__main__":
    print(get_input_template(1))
