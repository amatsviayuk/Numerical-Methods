import math
from matplotlib import pyplot


# Function to read data from a file and convert it into a list of [x, y] pairs
def get_data(f):
    data = []
    for line in f:
        [x, y] = line.split(" ")
        data.append([float(x), float(y)])
    return data


# Function to create a Lagrange interpolation function based on given points
def interpolation_function(points):
    def f(x):
        result = 0
        for i in range(len(points)):
            [xi, yi] = points[i]
            base = 1
            for j in range(len(points)):
                if i == j:
                    continue
                else:
                    xj, yj = points[j]
                    base *= (float(x) - float(xj)) / float(float(xi) - float(xj))
            result += float(yi) * base
        return result
    return f


# Function to perform Lagrange interpolation on data from files and generate plots
def lagrange(knot_number, path, files):
    for i in files:
        print(i)
        f = open(path + "/" + i, 'r')
        data = get_data(f)

        # Select a subset of points for interpolation
        interpolation_data = data[0::knot_number]
        F = interpolation_function(interpolation_data)

        # Extract distance and height data for plotting
        distance = [i[0] for i in data]
        height = [i[1] for i in data]
        interpolated_height = [lambda x=x: F(float(x)) for [x, y] in data]

        train_distance = [i[0] for i in interpolation_data]
        train_height = [lambda x=x: F(float(x)) for [x, y] in interpolation_data]

        # Plot full dataset and interpolated function
        pyplot.figure()
        pyplot.semilogy(distance, height, 'blue', label='All data')
        pyplot.semilogy(distance, [t() for t in interpolated_height], color='red', label='Interpolating function')
        pyplot.semilogy(train_distance, [t() for t in train_height], 'green', label='Interpolation data')
        pyplot.legend()
        pyplot.ylabel('Height')
        pyplot.xlabel('Distance')
        pyplot.title('Approximation with Lagrange Interpolation, ' + str(len(interpolation_data)) + ' points')
        pyplot.grid()
        pyplot.savefig('charts/lagrange/Lagrange_O' + i + '.png')
        pyplot.close()

        # Plot a segment of the dataset to highlight interpolation without oscillations
        n = math.floor(len(distance) / 3)
        pyplot.figure()
        pyplot.semilogy(distance[n:2*n], height[n:2*n], 'blue', label='All data')
        pyplot.semilogy(distance[n:2*n], [t() for t in interpolated_height[n:2*n]], color='red',
                        label='Interpolating function')
        n = math.floor(len(interpolation_data) / 3)
        pyplot.semilogy(train_distance[n:2*n], [t() for t in train_height[n:2*n]], 'g.',
                        label='Interpolation data')
        pyplot.legend()
        pyplot.ylabel('Height')
        pyplot.xlabel('Distance')
        pyplot.title('Approximation with Lagrange Interpolation, ' + str(len(interpolation_data) / 3) + ' points')
        pyplot.grid()
        pyplot.savefig('charts/lagrange/Lagrange_NO' + i + '.png')
        pyplot.close()
