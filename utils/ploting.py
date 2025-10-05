from matplotlib import pyplot as plt


def plot_the_graph(outputFiles, input_file_directory , file_name="output.jpg"):
    """ plot the graph of energy vs step
    :param outputFiles: list of outputFile objects
    :param input_file_directory: directory to save the plot
    :param file_name: name of the plot file
    :return: None
    """
    data = [float(f.scf_done) for f in outputFiles if f.scf_done != "could not found"]
    plt.plot(data)
    plt.ylabel("Energy/AU")
    plt.xlabel("Step")
    plt.savefig(f"{input_file_directory}/" + file_name)
    plt.clf()


def plot_scatter(outputFiles, input_file_directory , file_name="scatter.jpg"):
    """ plot the scatter graph of energy vs step for not converged files
    :param outputFiles: list of outputFile objects
    :param input_file_directory: directory to save the plot
    :param file_name: name of the plot file
    :return: None
    """
    x_coords = []
    y_coords = []
    for index, j in enumerate(outputFiles):
        if j.is_converged == 0:
            x_coords.append(index+1)
            y_coords.append(float(j.scf_done))
            print(index,j.scf_done)

    plt.scatter(x_coords,y_coords)
    plt.ylabel("Energy/AU")
    plt.xlabel("Step")
    plt.savefig(f"{input_file_directory}/" + file_name)
    plt.clf()

