import re


class LogFileManager:
    """
    This class is responsible for reading and extracting data from Gaussian log files.
    It extracts optimized coordinates,
    SCF energy, and other relevant information.
    It also provides methods to check if the calculation converged and if the structure is optimized.
    Attributes:
        file (str): The name of the log file to be read.
        input_file_directory (str): The directory where the log file is located.
        text (str): The content of the log file.
        opt_coords (list): The optimized coordinates extracted from the log file.
        scf_done (str): The SCF energy extracted from the log file.
        is_converged (bool): Indicates if the calculation converged.
        is_optimized (bool): Indicates if the structure is optimized (no imaginary frequencies).
        z_matrix (str): The initial Z-matrix extracted from the log file.
        title (str): The title of the calculation extracted from the log file.
        optimized_parameters (str): The optimized parameters extracted from the log file.
    Methods:
        get_data(): Reads the log file and extracts relevant data.
        read_log(): Reads the content of the log file.
        is_valid(): Checks if the log file is a valid Gaussian log file.
        is_optimized_exp(): Checks if the structure is optimized based on frequencies.
        get_scf_done(): Extracts the SCF energy from the log file.
        finish(): Cleans up resources after data extraction.
        write_data_to_the_data_file(): Writes extracted data to a data file.
        is_not_converged(): Checks if the calculation did not converge.
        get_initial_z_matrix(): Extracts the initial Z-matrix from the log file.
        get_title(): Extracts the title of the calculation from the log file.
        get_optimized_parameters(): Extracts the optimized parameters from the log file.
        optimized_coordinates(): Extracts the optimized coordinates from the log file.
        last_lines(): Returns the last few lines of the log file for error checking.
        get_freq(): Placeholder for frequency extraction method.
    """
    def __init__(self, file_name, input_file_directory):
        self.file = file_name
        self.input_file_directory =input_file_directory
        self.scf_list = None
        self.get_data()

    def get_data(self):
        self.read_log()
        self.opt_coords = self.optimized_coordinates()
        self.get_scf_done()
        self.finish()


    def log_file_name(self):
        return self.input_file_directory + '/' + self.file[:-3] + "log"

    def read_log(self):
        with open(self.input_file_directory + '/' + self.file, 'r') as log:
            self.text = log.read()

    def is_valid(self):
        return "Gaussian" in self.text

    def is_optimized_exp(self):
        """Check if the structure is optimized based on frequencies.
        Returns:
            ""bool: True if the structure is optimized (no imaginary frequencies), False otherwise."""
        pattern = r"Frequencies --\s+(-?\d+\.\d+)"
        result = re.search(pattern, self.text)
        first_frequency = re.findall(r"(-?\d+\.\d+)", result.group())
        self.is_optimized = float(first_frequency[0]) > 0
        return float(first_frequency[0]) > 0

    def get_scf_done(self, only_last_struc=False):
        """Extract the SCF energy from the log file.
        the SCF energy is typically found in lines starting with "SCF Done: E(RB3LYP) = ..." likewise
        and the pattern is matched using regular expressions.
        last occurrence of the SCF energy is considered in case of multiple occurrences.
        Returns:
            str: The SCF energy as a string, or "could not found" if not found.
            """


        scf_match = re.findall(r'SCF Done: .*', self.text)
        if len(scf_match) == 0:
            scf_match = re.findall(r'Energy= .*', self.text)

        if only_last_struc == False:
            scf_list  = []
            for match in scf_match:
                scf_list.append(re.findall(r'-?\d+\.\d+', match)[0])
            self.scf_done = scf_list[-1]
            self.scf_list = scf_list
            return scf_list
        else:
            self.scf_done = re.findall(r'-?\d+\.\d+', scf_match[-1])[0]
            return self.scf_done





    def finish(self):
        """Cleans up resources after data extraction. as log can be large"""
        self.text = None


    def is_not_converged(self):
        # for energy calculations
        if "Convergence failure" in self.text:
            self.is_converged = False
            print("failed to converge")
            return True
        else:
            self.is_converged = True
            return False

    def get_initial_z_matrix(self):

        lines = self.text.split("\n")

        z_matrix_section = False
        z_matrix = ""

        for line in lines:
            if "Symbolic Z-matrix:" in line:
                z_matrix_section = True
                continue

            if z_matrix_section:
                if line.strip() == "" or "GradGradGradGrad" in line:
                    break
                z_matrix += line +"\n"

        self.z_matrix = z_matrix
        return z_matrix

    def get_title(self):

        pattern = r'\n[- ]+\n(.+?)\n[- ]+\n Symbolic Z-matrix:'
        match = re.search(pattern, self.text, re.DOTALL)
        if match:
            result = match.group(1).strip().split("\n")
            self.title = result[-1]
        else:
            self.title = "could not find"

    def get_optimized_parameters(self):
        #todo: only count till the length of atoms
        lines = self.text.split("\n")
        section = False
        parameters = ""

        for line in lines:
            if "!   Optimized Parameters   !" in line:
                section = True
                continue

            if section:
                if line.strip() == "" or "GradGradGradGradGradGradGradGradGradGradGradGradGradGradGradGradGradGrad" in line:
                    break
                parameters +=line +"\n"

        self.optimized_parameters = parameters
        return parameters

    def optimized_coordinates(self,only_last_struc=False):
        """Extract the optimized coordinates from the log file.
        the optimized coordinates are typically found in the "Standard orientation" section of the log file.
        The method uses regular expressions to locate and extract the coordinates.

        Returns:
            list: A list of optimized coordinates, where each coordinate is represented as a list of floats [x, y, z].
        """


        # Define the regex pattern to find the "Standard orientation" section
        pattern = re.compile(
            r'Input orientation:[\s\S]*?---------------------------------------------------------------------[\s\S]*?---------------------------------------------------------------------([\s\S]*?)---------------------------------------------------------------------')

        # Search for the pattern
        matches = pattern.findall(self.text)
        coordinates_section = matches[-1].strip()
        if matches:
            if only_last_struc == True:
                coordinates = []

                # Extract coordinates using regex
                coord_pattern = re.compile(r'^\s*\d+\s+\d+\s+\d+\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)',
                                           re.MULTILINE)
                for coord_match in coord_pattern.finditer(coordinates_section):
                    x, y, z = map(float, coord_match.groups())
                    coordinates.append([x, y, z])
                return coordinates
            else:
                all_intermediates =[]
                for coord in matches:
                    coordinates = []
                    coord_pattern = re.compile(r'^\s*\d+\s+\d+\s+\d+\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)',
                                               re.MULTILINE)
                    for coord_match in coord_pattern.finditer(coord):
                        x, y, z = map(float, coord_match.groups())
                        coordinates.append([x, y, z])
                    all_intermediates.append(coordinates)
                return all_intermediates


        else:
            raise ValueError("Optimized coordinates section not found in the log file")

    def last_lines(self):
        """Returns the last few lines of the log file for error checking."""

        lines=""

        with open(self.log_file_name(), 'r') as file:
            read = file.readlines()
            for line in range(-10,-3):
                lines+=str(read[line])
        return lines

    def get_freq(self):
        pass


