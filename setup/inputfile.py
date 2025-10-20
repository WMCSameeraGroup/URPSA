from atoms.atoms import Atom
from calculations.random_spherical_coords_generator import random_spherical_coordinates_generator, \
    generate_random_point_on_sphere
from molecule.molecule import Molecule
from setup.inputFileParser import CustomConfigParser


class InputFile:
    """
    Extracting data from a given input file and filling with default values.
    """

    # get the data from the input file provided or get the missing values from the defaults.py file
    def __init__(self, file):
        """
        :param file: String (path to input file)
        :Attributes:
            file (str): path to the input file
            config (CustomConfigParser): ConfigParser object to read the input file
            project_name (str): name of the project
            sphere_radius (float): radius of the sphere
            step_size (float): step size for pushing molecules
            step_count (int): number of steps to push molecules
            stop_distance_factor (float): factor to determine when to stop pushing molecules
            charge (int): total charge of the system
            multiplicity (int): multiplicity of the system
            number_of_molecules (int): number of different molecules in the system
            n_iterations (int): number of iterations to perform
            consecutive_duplicates_threshold (int): threshold for consecutive duplicate products
            stress_release (list): list of iterations where stress release is applied
            spherical_placement (str): method for placing molecules on the sphere
            method (str): computational method to be used in Gaussian calculations
            cores (str): number of CPU cores to be used in Gaussian calculations
            memory (str): amount of memory to be used in Gaussian calculations
            list_of_molecules (list): list of Molecule objects representing the molecules in the system
            update_with_optimized_coordinates (str): whether to update coordinates with optimized ones from Gaussian
            is_placed_on_sphere (bool): whether molecules are placed on the sphere
            additional_constraints (str): additional constraints for Gaussian calculations
            ADD_COM_CONST (str): whether to add center of mass constraints
            ADD_SPHERICAL_CONST (str): whether to add spherical constraints
            dynamic_fragment_replacement (str): whether to enable dynamic fragment replacement
            cutoff_energy_gap (float): energy gap threshold for considering a pathway valid
            energy_surpass_options (str): options for handling energy surpass situations ("optimize" or "exit")
            optimize_the_final_particle (str): whether to optimize the final particle after placement
            convergence_error (str): action to take on convergence error ("exit" or "continue")
            unsuccessful_pathway (str): action to take on unsuccessful pathway ("exit" or "continue")
            lattice (Molecule or str): lattice structure if provided, otherwise an empty string
        """

        self.count_of_atom = 1
        self.file = file
        self.config = CustomConfigParser()
        self.config.read(self.file)
        self.project_name = self.config.get('project', 'project_name')
        self.sphere_radius = float(self.config.get('controls', 'sphere_radius'))
        self.step_size = float(self.config.get('controls', 'step_size'))
        self.step_count = int(self.config.get('controls', 'step_count'))
        self.stop_distance_factor = float(self.config.get('controls', 'stop_distance_factor'))
        self.charge = int(float(self.config.get('molecules', 'charge')))
        self.multiplicity = int(float(self.config.get('molecules', 'multiplicity')))
        self.number_of_molecules = int(self.config.get('molecules', 'number_of_molecules'))
        self.n_iterations = int(self.config.get('controls', 'n_iterations'))
        self.consecutive_duplicates_threshold = int(self.config.get('controls', 'consecutive_duplicates_threshold'))
        self.stress_release = self.set_stress_release()
        self.spherical_placement = self.config.get('controls', 'spherical_placement')
        self.method = self.config.get('gaussian', 'method')
        self.cores = self.config.get('gaussian', 'number_of_cores')
        self.memory = self.config.get('gaussian', 'memory')

        self.list_of_molecules = self.set_molecule_list()
        # update with
        self.update_with_optimized_coordinates = self.config.get('controls', 'update_with_optimized_coordinates')
        self.is_placed_on_sphere = self.create_spherically_located_molecule_list()
        self.additional_constraints = self.set_additional_constraints()
        self.ADD_COM_CONST = self.config.get("controls", "ADD_COM_CONST")
        self.ADD_SPHERICAL_CONST = self.config.get("controls", "ADD_SPHERICAL_CONST")
        self.fragment_detection_factor = float(self.config.get('controls', 'fragment_detection_factor'))
        self.dynamic_fragment_replacement = self.config.get("controls", "dynamic_fragment_replacement")
        self.cutoff_energy_gap = float(self.config.get("controls", "cutoff_energy_gap"))
        self.energy_surpass_options = self.config.get("controls", "energy_surpass_options")
        self.optimize_the_final_particle =self.config.get('controls', 'optimize_the_final_particle')
        self.convergence_error = self.config.get('controls', 'convergence_error')
        self.unsuccessful_pathway = self.config.get('controls', 'unsuccessful_pathway')
        self.lattice = self.get_lattice()
        print(self.lattice)


    def get_lattice(self):
        """
        get the lattice from the input file if provided
        this is optional and can be used for when a fixed structure is needed to perform the calculations on top of it.
        :rtype: Molecule
        1. if lattice is provided in the input file, convert it to a Molecule object and return it
        2. if lattice is not provided, return an empty string
        3. example:
        lattice:
        C 0.0 0.0 0.0
        H 0.0 0.0 1.0
        H 1.0 0.0 0.0
        :return:
        """
        string = self.config.get('molecules', 'lattice')

        atom_list = []
        if string:
            for line in string.split("\n"):
                line_data = line.split()
                if len(line_data) >= 4:  # linear convergence
                    atom_list.append(Atom(*line_data,self.count_of_atom))
                    self.count_of_atom += 1

            lattice = Molecule(atom_list)

            return lattice
        else:
            return ""





    def set_molecule_list(self):
        """
        get the list of molecules from the input file and convert them to Molecule objects
        :rtype: list
        1. loop over the number of molecules
        2. get the string of each molecule from the input file
        3. convert the string to a Molecule object using set_molecule method
        4. append the Molecule object to the list
        5. return the list of Molecule objects
        :return:[molecule]: list of Molecule objects
        """
        molecule_list = []
        for n in range(self.number_of_molecules):
            string = self.config.get('molecules', str(n))
            molecule_list.append(self.set_molecule(string))

        self.list_of_molecules = molecule_list
        self.count_of_atom = 1
        return molecule_list

    def set_additional_constraints(self):
        """
        get string of constraints from the input file and modify it by changing /- to = this
        :return (Str): String of constraints
        """
        if self.config.get('Additional', "constraints"):
            string = self.config.get('Additional', "constraints").replace("/-", "=")
            return string

    def set_molecule(self, string):
        """
        converts string of data to molecule object

        :param string: input string
        :return: Molecule object
        """
        atom_list = []
        for line in string.split("\n"):
            line_data = line.split()
            if len(line_data) >= 4:  # linear convergence
                atom_list.append(Atom(*line_data, self.count_of_atom))
                self.count_of_atom += 1

            else:
                print("incorrect atom format in input file ")
        return Molecule(atom_list)

    def create_spherically_located_molecule_list(self):
        """
        tell what method is used to positions molecules into new random positions of a sphere
        and modify molecular coordinates.
        if self.spherical_placement == "False"  then it doesn't modify coordinates.

        Modify: Molecule object positions
        :return Boolean:
        """

        if self.spherical_placement == "False":
            return False
        for molecule in self.list_of_molecules:
            if self.spherical_placement == "Total_random":
                molecule.update_coordinates(*random_spherical_coordinates_generator(self.sphere_radius))
            elif self.spherical_placement == "statistically_even":
                molecule.update_coordinates(*generate_random_point_on_sphere(self.sphere_radius))
        return True

    def set_stress_release(self):
        """
        get data from 'controls', 'stress_release' and build a list of numbers with start, step and end.
        :return list: list of int which says not to put constraints into the optimization.
        """
        comm = self.config.get('controls', 'stress_release')
        start = comm.split(":")[0]
        step = comm.split(":")[1]
        end = comm.split(":")[2]
        return [i for i in range(int(start), int(end), int(step))]


if __name__ == "__main__":
    print(InputFile('../exampleInput.txt').list_of_molecules)
