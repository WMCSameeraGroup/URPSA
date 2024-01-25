import re
from settings import data_file_name
class LogFileManager:
    def get_data(self):
        self.read_log()
        if self.is_valid():

            if self.is_optimized():
                if self.is_converged():
                    self.get_scf_done()
                    self.write_data_to_the_data_file()
                    self.finish()
                else:
                    print("calculation is not converged properly there is/are imaginary frequencies")
            else:
                print("calculation is not optimized")

    def read_log(self):
        with open(self.file, 'r') as log:
            self.text = log.read()

    def __init__(self, file_name):
        self.file = file_name
        self.get_data()

    def is_valid(self):
        return "Gaussian" in self.text

    def is_converged(self):
        return "Optimization completed" in self.text

    def is_optimized(self):
        # Check if the geometry is optimized

        pattern = r"Frequencies --\s+(-?\d+\.\d+)"
        result = re.search(pattern, self.text)
        first_frequency = re.findall(r"(-?\d+\.\d+)", result.group())

        return float(first_frequency[0]) > 0

    def get_scf_done(self):
        scf_match = re.findall(r'SCF Done: .*', self.text)

        if scf_match:
            self.scf_done = re.findall(r'-\d+.\d+', scf_match[-2])
            # print(self.scf_done)
            return self.scf_done

    def finish(self):
        self.text = None

    def write_data_to_the_data_file(self):
        with open(data_file_name,'a') as file:
            file.write(f"{self.file}\t{self.scf_done}")



if __name__ == '__main__':
    file_name = "logfile.log"
    log_file = LogFileManager(file_name)

