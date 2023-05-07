import numpy as np
import re
from OpenCv import ocr
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from mpl_toolkits.mplot3d import Axes3D
import scipy.linalg
import sys


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
        # Remove spaces from the equation
        equation = equation.replace(" ", "")
        # Create a matrix of coefficients from the array of equations.
        matches = re.findall(var_regex, equation)
        coeffs = []
        for match in matches:
            coeff = match[0] if match[0] else "+1" if match[1] != '-' else "-1"
            coeffs.append(int(coeff))
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

# Parametric solver is meant to solve linear systems from an array of linear equations.
# This solution was "borrowed" from https://stackoverflow.com/questions/54971085/how-to-solve-linear-equations-with-parametrization


def parametric_form(a, b):
    one_solution = np.linalg.lstsq(a, b, rcond=None)[0]
    null_space_basis = scipy.linalg.null_space(a)
    for i in range(a.shape[1]):
        sys.stdout.write('x{} = {}'.format(i, one_solution[i]))
        for j in range(null_space_basis.shape[1]):
            sys.stdout.write(' + ({}) * t{}'.format(null_space_basis[i, j], j))
        sys.stdout.write('\n')
    return


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
        ax.plot_surface(X, Y, Z, cmap='cool', alpha=0.7)
    # Add solution to z
    sol = np.linalg.solve(coefficient_matrix, constant_matrix)
    # Plot the solution to the system.
    ax.scatter(sol[0], sol[1], sol[2], c='r', s=30)
    ax.text(sol[0], sol[1], sol[2], 'Solution', color='r', fontsize=12)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


# This function is meant to plot the solution to a system of equations when matrix A is singular.
def singular_plotter(coefficient_matrix, constant_matrix):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    colors = ['hsv', 'pink']
    for i in range(coefficient_matrix.shape[0]):
        eq = coefficient_matrix[i]
        const = constant_matrix[i]
        x = np.linspace(-10, 10, 100)
        y = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x, y)
        Z = (const - eq[0] * X - eq[1] * Y) / eq[2]
        # Calculate the index of the color to use
        color_index = i % len(colors)
        ax.plot_surface(X, Y, Z, cmap=colors[color_index], alpha=0.8)
    # Plot the solution to the system.
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


def plotter_main(equations=[]):
    if len(equations) == 0:
        print("No equations were provided.")
        return
    if len(equations) > 3:
        print("The program can only plot up to 3 equations.")
        return
    coefficient_matrix, constant_matrix = matrix_generator(equations)
    if np.linalg.det(coefficient_matrix) < 0.0001:
        singular_plotter(coefficient_matrix, constant_matrix)
        return
    plotter(coefficient_matrix, constant_matrix)
    return


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
    # Testing push
    print(equation_solver(
        ['2x + 3y + 4z = 5', '4x + 6y + 8z = 10', '10x - 5y + 6z = 7']))
    print(matrix_generator(
        ['2x + 3y + 4z = 5', 'x - 4y + 5z = 6', '4x + 2y + 6z = 7']))
    singular_plotter(
        np.array([[1, 2, 3], [2, 4, 6], [3, 6, 9]]), np.array([[1], [2], [3]]))
    return


main()
