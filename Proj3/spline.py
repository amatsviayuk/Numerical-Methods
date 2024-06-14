from matplotlib import pyplot


# Function to create a square matrix of given size, with 'a1' on the diagonal and 0 elsewhere
def createMatrix(size, a1):
    mat = []
    for i in range(size):
        row_list = []
        for j in range(size):
            if i == j:
                row_list.append(a1)
            else:
                row_list.append(0)
        mat.append(row_list)
    return mat


# Function to create a copy of a given matrix A
def copy_matrix(A):
    copy = []
    for row in A:
        new_row = []
        for element in row:
            new_row.append(element)
        copy.append(new_row)
    return copy


# Function to perform LU decomposition and solve the system of equations
def LU(A, b):
    size = len(A)  # Determine the size of the matrix
    U = copy_matrix(A)  # Create a copy of matrix A for U
    L = createMatrix(size, 1)  # Initialize L as an identity matrix

    x = [1 for i in range(size)]  # Initialize solution vector x
    y = [0 for i in range(size)]  # Initialize intermediate solution vector y

    # Perform LU decomposition
    for i in range(size):
        for j in range(i + 1, size):
            L[j][i] = U[j][i] / U[i][i]
            for z in range(i, size):
                U[j][z] -= L[j][i] * U[i][z]

    # Solve Ly = b using forward substitution
    for i in range(size):
        S = 0
        for j in range(i):
            S += L[i][j] * y[j]
        y[i] = (b[i] - S) / L[i][i]

    # Solve Ux = y using backward substitution
    for i in range(size - 1, -1, -1):
        S = 0
        for j in range(i + 1, size):
            S += U[i][j] * x[j]
        x[i] = (y[i] - S) / U[i][i]

    return x  # Return the solution vector x


# Function to read data from a file and convert it into a list of [x, y] pairs
def get_data(f):
    data = []
    for line in f:
        [x, y] = line.split(" ")
        data.append([float(x), float(y)])
    return data


# Function to create a cubic spline interpolation function based on given data
def interpolation_function(data):
    def calculate_params():
        n = len(data)

        # Initialize the matrix A and vector b for solving the spline coefficients
        A = createMatrix(4 * (n - 1), 0)
        b = [0 for i in range((4 * (n - 1)))]

        # Set up equations based on data points
        for i in range(n - 1):
            [x, y] = data[i]
            row = [0 for i in range((4 * (n - 1)))]
            row[4 * i + 3] = 1
            A[4 * i + 3] = row
            b[4 * i + 3] = float(y)

        for i in range(n - 1):
            x1, y1 = data[i + 1]
            x0, y0 = data[i]
            h = float(x1) - float(x0)
            row = [0 for i in range((4 * (n - 1)))]
            row[4 * i] = h ** 3
            row[4 * i + 1] = h ** 2
            row[4 * i + 2] = h ** 1
            row[4 * i + 3] = 1
            A[4 * i + 2] = row
            b[4 * i + 2] = float(y1)

        # Continuity conditions for first and second derivatives
        for i in range(n - 2):
            x1, y1 = data[i + 1]
            x0, y0 = data[i]
            h = float(x1) - float(x0)
            row = [0 for i in range((4 * (n - 1)))]
            row[4 * i] = 3 * (h ** 2)
            row[4 * i + 1] = 2 * h
            row[4 * i + 2] = 1
            row[4 * (i + 1) + 2] = -1
            A[4 * i] = row
            b[4 * i] = 0

        for i in range(n - 2):
            x1, y1 = data[i + 1]
            x0, y0 = data[i]
            h = float(x1) - float(x0)
            row = [0 for i in range((4 * (n - 1)))]
            row[4 * i] = 6 * h
            row[4 * i + 1] = 2
            row[4 * (i + 1) + 1] = -2
            A[4 * (i + 1) + 1] = row
            b[4 * (i + 1) + 1] = 0

        # Natural spline boundary conditions
        row = [0 for i in range((4 * (n - 1)))]
        row[1] = 2
        A[1] = row
        b[1] = 0

        row = [0 for i in range((4 * (n - 1)))]
        x1, y1 = data[-1]
        x0, y0 = data[-2]
        h = float(x1) - float(x0)
        row[1] = 2
        row[-4] = 6 * h
        A[-4] = row
        b[-4] = 0

        # Solve for the spline coefficients
        result = LU(A, b)
        return result

    # Calculate the parameters of the spline
    params = calculate_params()

    def f(x):
        param_array = []
        row = []
        for param in params:
            row.append(param)
            if len(row) == 4:
                param_array.append(row.copy())
                row.clear()

        for i in range(1, len(data)):
            xi, yi = data[i-1]
            xj, yj = data[i]
            if float(xi) <= x <= float(xj):
                a, b, c, d = param_array[i-1]
                h = x - float(xi)
                return a*(h**3) + b*(h**2) + c*h + d
    return f


# Function to perform spline interpolation on data from files and generate plots
def spline(knot_number, path, files):
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
        interpolated_height = [F(float(x)) for x, _ in data]  # Interpolating function for each point

        train_distance = [i[0] for i in interpolation_data]
        train_height = [i[1] for i in interpolation_data]

        # Plot full dataset, interpolation points, and interpolating function
        pyplot.figure()
        pyplot.plot(distance, height, 'blue', label='All data')
        pyplot.plot(train_distance, train_height, 'go', label='Interpolation points')  # Interpolation points
        pyplot.plot(distance, interpolated_height, 'red', label='Interpolating function')  # Interpolating function
        pyplot.legend()
        pyplot.xlabel('Distance')
        pyplot.ylabel('Height')
        pyplot.title('Approximation with Spline Interpolation, ' + str(len(interpolation_data)) + ' points')
        pyplot.grid()
        pyplot.savefig('charts/spline/Spline_' + i + '.png')
        pyplot.close()
