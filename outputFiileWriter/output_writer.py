class OutputWriter:
        """
        Handles writing output files in XYZ format.

        Attributes:
            file (str): Path to the output file.
        """

        def __init__(self, input_file_directory, file="output2.xyz"):
            """
            Initializes OutputWriter with a directory and optional filename.

            Args:
                input_file_directory (str): Directory for the output file.
                file (str, optional): Name of the output file. Defaults to "output2.xyz".
            """
            self.file = input_file_directory + "/" + file

        def create_if_not(self):
            """
            Ensures the output file exists. Creates it if it does not.
            """
            try:
                with open(self.file, "a") as _:
                    pass
            except:
                with open(self.file, "w") as _:
                    pass

        def write_xyz_file(self, sys, opt_xyz: str):
            """
            Writes optimized coordinates to the output file in XYZ format.

            Args:
                sys: Object with string_optimized_coordinates method.
                opt_xyz: Optimized coordinates to write.
            """
            self.create_if_not()
            with open(self.file, "a") as f:
                f.write(sys.string_optimized_coordinates(opt_xyz))