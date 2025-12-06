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

    y_coords = []
    for  j in outputFiles:
        if j.is_converged == 0:
            y_coords.extend([float(val) for val in j.scf_list])

    x_coords = [i for i in range(len(y_coords))]


    plt.scatter(x_coords,y_coords)
    plt.ylabel("Energy/AU")
    plt.xlabel("Step")
    plt.savefig(f"{input_file_directory}/" + file_name)
    plt.clf()

