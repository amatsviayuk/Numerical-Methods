from plots import *
from os import listdir
from os.path import isfile, join


if __name__ == "__main__":
    # Define the number of knots and the path to the data files
    knot = 10
    path = "./data"

    # List all files in the directory
    files = [f for f in listdir(path) if isfile(join(path, f))]

    plots_with_input_data(path, files)  # create input
    spline(knot, path, files)  # spline
    lagrange(knot, path, files)  # lagrange
