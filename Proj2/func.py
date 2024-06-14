from copy import deepcopy
import math


def createMatrix(N, a1, a2, a3):
    matrix = [[0 for i in range(N)] for j in range(N)]

    for i in range(N):
        matrix[i][i] = a1
        if i > 0:
            matrix[i][i - 1] = matrix[i - 1][i] = a2
        if i > 1:
            matrix[i][i - 2] = matrix[i - 2][i] = a3
    return matrix


def residual(matrix_A, vector_b, vector_x):
    size = len(vector_b)
    residual_vector = [0 for _ in range(size)]
    for i in range(size):
        residual_vector[i] = vector_b[i]
        for j in range(size):
            residual_vector[i] -= matrix_A[i][j] * vector_x[j]
    return residual_vector


def norm(v):
    return math.sqrt(sum([i * i for i in v]))


def Jacobi(matrix_A, vector_b, error):
    size = len(vector_b)
    counter = 0
    vector_x = [1 for _ in range(size)]
    vector_x_new = [1 for _ in range(size)]
    residuum = []
    while True:
        for i in range(size):
            vector_x_new[i] = vector_b[i]
            for j in range(size):
                if i != j:
                    vector_x_new[i] -= matrix_A[i][j] * vector_x[j]
            vector_x_new[i] /= matrix_A[i][i]
        vector_x = vector_x_new.copy()
        residual_vector = residual(matrix_A, vector_b, vector_x)
        res_norm = norm(residual_vector)
        if res_norm < error or counter > 1000:
            break
        counter += 1
        residuum.append(res_norm)
    return residuum, counter


def Gauss_Seidel(matrix_A, vector_b, error):
    size = len(vector_b)
    counter = 0
    vector_x = [1 for _ in range(size)]
    vector_x_new = [1 for _ in range(size)]
    residuum = []
    while True:
        for i in range(size):
            vector_x_new[i] = vector_b[i]
            for j in range(size):
                if i != j:
                    vector_x_new[i] -= matrix_A[i][j] * vector_x_new[j]
            vector_x_new[i] /= matrix_A[i][i]
        vector_x = vector_x_new.copy()
        residual_vector = residual(matrix_A, vector_b, vector_x)
        res_norm = norm(residual_vector)
        if res_norm < error or counter > 1000:
            break
        counter += 1
        residuum.append(res_norm)
    return residuum, counter


def LU(A, b):
    U = deepcopy(A)
    L = eye(len(A))
    solution = [1 for i in range(len(A))]
    intermediary_vector = [0 for i in range(len(A))]

    # LU decomposition
    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            L[j][i] = U[j][i] / U[i][i]
            for k in range(i, len(A)):
                U[j][k] -= L[j][i] * U[i][k]

    # Forward substitution (Ly = b)
    for i in range(len(A)):
        intermediary_vector[i] = b[i]
        for j in range(i):
            intermediary_vector[i] -= L[i][j] * intermediary_vector[j]
        intermediary_vector[i] /= L[i][i]

    # Back substitution (Ux = y)
    for i in range(len(A) - 1, -1, -1):
        solution[i] = intermediary_vector[i]
        for j in range(i + 1, len(A)):
            solution[i] -= U[i][j] * solution[j]
        solution[i] /= U[i][i]

    # Calculate the norm of the residual
    residual_norm = norm(residual(A, b, solution))

    return residual_norm


def eye(size):
    return [[1 if i == j else 0 for i in range(size)] for j in range(size)]
