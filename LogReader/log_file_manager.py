import re
from settings import data_file_name, input_file_directory


class LogFileManager:
    def get_data(self):
        self.read_log()
        self.get_scf_done()
        self.write_data_to_the_data_file()
        self.is_not_converged()
        self.finish()

    def log_file_name(self):
        return input_file_directory + '/' + self.file[:-3] + "log"

    def read_log(self):
        with open(input_file_directory + '/' + self.file, 'r') as log:
            self.text = log.read()

    def __init__(self, file_name):
        self.file = file_name
        self.get_data()

    def is_valid(self):
        return "Gaussian" in self.text


    def is_optimized(self):
        # Check if the geometry is optimized
        pattern = r"Frequencies --\s+(-?\d+\.\d+)"
        result = re.search(pattern, self.text)
        first_frequency = re.findall(r"(-?\d+\.\d+)", result.group())
        return float(first_frequency[0]) > 0

    def get_scf_done(self):
        scf_match = re.findall(r'SCF Done: .*', self.text)

        if scf_match:
            self.scf_done = re.findall(r'-\d+.\d+', scf_match[-1])
            return self.scf_done
        else:
            self.scf_done = "could not found"

    def finish(self):
        self.text = None

    def write_data_to_the_data_file(self):
        with open(data_file_name, 'a') as file:
            file.write(f"{self.file}\t{self.scf_done} \n")

    def is_not_converged(self):
        if "Convergence failure" in self.text:
            print("failed to converge")
            return True
        else:
            return False


if __name__ == '__main__':
    file_name = "logfile.log"
    log_file = LogFileManager(file_name)

# todo: write to a csv file instead of a text/ transfer chk and outputs to a different directory


