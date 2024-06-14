from settings import input_file_directory


class OutputWriter:

    def __init__(self, file="output2.xyz"):
        self.file = input_file_directory + "/" + file

    def create_if_not(self):
        try:
            with open(self.file, "a") as _:
                pass
        except:
            with open(self.file, "w") as _:
                pass

    # def write_output_file(self, log_manager):
    #     self.create_if_not()
    #     with open(self.file, "a") as f:
    #         f.write("----------------------------------------------------------------\n")
    #         # f.write("\n")
    #         # f.write(log_manager.title)
    #         # f.write("\n")
    #         # f.write(log_manager.z_matrix)
    #         # f.write("\n")
    #         # f.write(log_manager.scf_done[0])
    #         # f.write("\n")
    #         # # f.write(log_manager.is_optimized)
    #         # f.write(log_manager.optimized_parameters)
    #         # f.write("\n")
    #         # f.write(log_manager.optmized_z_matrix)
    #         # f.write("\n")
    #         f.write("----------------------------------------------------------------\n")

    def write_xyz_file(self,sys):
        self.create_if_not()
        with open(self.file, "a") as f:
            f.write(sys.to_str())

