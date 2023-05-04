import numpy as np
import re
from OpenCv import ocr
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from mpl_toolkits.mplot3d import Axes3D

# This function is meant to solve linear systems from an array of linear equations.
# It will return the solution to the system in parametric form.
# The function will also return the number of solutions to the system, if any.


def matrix_generator(equations=[]):
    var_regex = r'([-+]?\d*)([a-z])'
    const_regex = r'([-+]?\d+)$'

    # Obtain the number of equations from the array of equations.
    num_equations = len(equations)
    # Obtain the number of variables from the array of equations.
    coefficient_matrix = np.zeros((num_equations, num_equations))
    constant_matrix = np.zeros((num_equations, 1))
    for i in range(num_equations):
        equation = equations[i]
        # Create a matrix of coefficients from the array of equations.
        matches = re.findall(var_regex, equation)
        coeffs = [int(match[0]) if match[0] else 1 if match[1]
                  else 0 for match in matches]
        coeffs = np.array(coeffs)
        # Create a matrix of constants from the array of equations.
        constant = re.findall(const_regex, equation)
        constants = np.array([int(constant[0])])
        # Add the coefficients to the matrix of coefficients.
        coefficient_matrix[i, :] = coeffs
        # Add the constants to the matrix of constants.
        constant_matrix[i, :] = constants
    return coefficient_matrix, constant_matrix


def equation_solver(equations=[]):
    coefficient_matrix, constant_matrix = matrix_generator(equations)
    # Check if the determinant of the coefficient matrix is 0. Floating point error is accounted for.
    if np.linalg.det(coefficient_matrix) < 0.0001:
        parametric_form(coefficient_matrix, constant_matrix)
        return
    solution = np.linalg.solve(coefficient_matrix, constant_matrix)
    return solution

# This function is meant to solve linear systems from an array of linear equations when the system is in augmented form.


def parametric_form(A, b):
    # Compute the SVD of A
    U, S, V = np.linalg.svd(A)

    # Find the index of the smallest singular value
    idx = np.argmin(S)

    # Extract the null space of A
    null_space = V[idx:].T

    # Compute the particular solution
    x_particular = np.linalg.pinv(A).dot(b)

    # Write the system in parametric form
    t = np.linspace(-10, 10, 100)  # Choose a range of values for t
    solution_space = null_space.dot(t) + x_particular[:, np.newaxis]

    # Print the parametric form
    for i, var in enumerate(['x', 'y', 'z']):
        print("{} = {:.2f}t + {:.2f}".format(var,
              solution_space[i, 0], solution_space[i, 1]))

# This function is meant to plot the solution to a system of equations in parametric form.
# Note that this requires the equation to be written in a certain way, i.e 2x + 3y + 4z = 5.
# -(With z being the third variable), the X and Y can be reversed, but the Z must be the third variable.
# To avoid this, the equation solver would have to keep track of the Z coefficient.


def plotter(coefficient_matrix, constant_matrix):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(coefficient_matrix.shape[0]):
        eq = coefficient_matrix[i]
        const = constant_matrix[i]
        x = np.linspace(-10, 10, 100)
        y = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x, y)
        Z = (const - eq[0]*X - eq[1]*Y) / eq[2]
        ax.plot_surface(X, Y, Z, cmap='cool', alpha=0.5)
    # Add solution to z
    sol = np.linalg.solve(coefficient_matrix, constant_matrix)
    # Plot the solution to the system.
    ax.scatter(sol[0], sol[1], sol[2], c='r', s=30)
    ax.text(sol[0], sol[1], sol[2], 'Solution', color='r', fontsize=12)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


def ocr_solve(file_name):
    img, equations = ocr(file_name)
    solution = equation_solver(equations)
    return solution


def only_eq_solve(equations):
    solution = equation_solver(equations)
    return solution


def main():
    # Test the function.
    # equations = ['2x + 3y + 4z = 5', '3x + 4y + 5z = 6', '4x + 5y + 6z = 7']
    # Check if determinant is 0
    # print(ocr_solve("pic.png"))
    plotter(np.array([[1, 2, 3], [4, 1, 5], [7, 3, 9]]), np.array([1, 6, 3]))
    return


main()
