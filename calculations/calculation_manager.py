from settings import input_file_directory,backend
import subprocess


def run_calculation(input_file): # todo: change commands to orca as well
    if backend == "g16":
        gaussian_command = "g16 " +input_file_directory +'/'+ input_file

        try:
            print("running " + input_file)
            # Run Gaussian using subprocess
            process = subprocess.run(gaussian_command, shell=True, check=True, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, text=True)

            # Check if the Gaussian job completed successfully
            if process.returncode == 0:
                print("Gaussian job completed successfully.- {0}".format(input_file))
                return 0

            else:
                print("Error running Gaussian job.")
                print("Error message:\n", process.stderr)
                return -1

        except subprocess.CalledProcessError as e:
            print("Error running Gaussian job.")
            #print("Error message:\n", e.stderr)
            return -2
