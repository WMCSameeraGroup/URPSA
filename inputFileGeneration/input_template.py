def get_input_template(number, system,inp_dir):
    """ Generate Gaussian input file template.
    :param number: int, the step number
    :param system: System object containing method, charge, multiplicity, number_of_cores
    :param inp_dir: str, directory to save checkpoint file
    :return: str, formatted Gaussian input file template
    """
    return f"""%NProcShared={system.number_of_cores}
%Mem={system.memory}
%chk={inp_dir}/test{number}.chk
{system.method}

step{number}
 
{system.charge} {system.multiplicity}	\n"""


