from settings import output_file_directory
import subprocess


def run_calculation(input_file):
    gaussian_command = "g16 " +output_file_directory +'/'+ input_file +" &"

    try:
        print("running " + input_file)
        # Run Gaussian using subprocess
        process = subprocess.run(gaussian_command, shell=True, check=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, text=True)

        # Check if the Gaussian job completed successfully
        if process.returncode == 0:
            print("Gaussian job completed successfully.- {0}".format(input_file))

        else:
            print("Error running Gaussian job.")
            print("Error message:\n", process.stderr)

    except subprocess.CalledProcessError as e:
        print("Error running Gaussian job.")
        print("Error message:\n", e.stderr)
