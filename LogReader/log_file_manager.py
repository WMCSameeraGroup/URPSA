import re
from settings import data_file_name, input_file_directory


class LogFileManager:
    def __init__(self, file_name):
        self.file = file_name
        self.get_data()

    def get_data(self):
        self.read_log()
        self.opt_coords = self.optimized_coordinates()
        self.get_scf_done()
        self.finish()


    def log_file_name(self):
        return input_file_directory + '/' + self.file[:-3] + "log"

    def read_log(self):
        with open(input_file_directory + '/' + self.file, 'r') as log:
            self.text = log.read()

    def is_valid(self):
        return "Gaussian" in self.text

    def is_optimized_exp(self):
        # Check if the geometry is optimized
        # todo: fix this
        pattern = r"Frequencies --\s+(-?\d+\.\d+)"
        result = re.search(pattern, self.text)
        first_frequency = re.findall(r"(-?\d+\.\d+)", result.group())
        self.is_optimized = float(first_frequency[0]) > 0
        return float(first_frequency[0]) > 0

    def get_scf_done(self):
        scf_match = re.findall(r'SCF Done: .*', self.text)

        if scf_match:
            self.scf_done = re.findall(r'-\d+.\d+', scf_match[-1])
            print(self.scf_done)
            return self.scf_done
        else:
            self.scf_done = "could not found"

    def finish(self):
        self.text = None

    def write_data_to_the_data_file(self):
        with open(data_file_name, 'a') as file:
            file.write(f"{self.file}\t{self.scf_done} \n")

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

    def optimized_coordinates(self):
        coordinates = []
        # Define the regex pattern to find the "Standard orientation" section
        pattern = re.compile(
            r'Standard orientation:[\s\S]*?---------------------------------------------------------------------[\s\S]*?---------------------------------------------------------------------([\s\S]*?)---------------------------------------------------------------------')

        # Search for the pattern
        match = pattern.search(self.text)
        if match:
            coordinates_section = match.group(1).strip()
            # Extract coordinates using regex
            coord_pattern = re.compile(r'^\s*\d+\s+\d+\s+\d+\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)',
                                       re.MULTILINE)
            for coord_match in coord_pattern.finditer(coordinates_section):
                x, y, z = map(float, coord_match.groups())
                coordinates.append([x, y, z])
            return coordinates
        else:
            raise ValueError("Optimized coordinates section not found in the log file")

