from lagrange import *
from spline import *


def plots_with_input_data(path, files):
    for i in files:
        f = open(path + "/" + i, 'r')  # Open each file
        data = get_data(f)  # Extract data from the file

        # Separate data into distance and height lists
        distance = [i[0] for i in data]
        height = [i[1] for i in data]

        # Create the plot
        pyplot.figure()
        pyplot.plot(distance, height, 'blue', label='All data')
        pyplot.legend()
        pyplot.xlabel('Distance')
        pyplot.ylabel('Height')
        pyplot.title(str(len(data)) + ' points')
        pyplot.suptitle(i)
        pyplot.grid()

        # Save the plot
        pyplot.savefig('charts/profile_altitudes/' + i + '.png')
        pyplot.close()
