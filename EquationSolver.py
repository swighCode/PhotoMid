import numpy as np
import re
from OpenCv import ocr

# This function is meant to solve linear systems from an array of linear equations.
# It will return the solution to the system in parametric form.
# The function will also return the number of solutions to the system, if any.


def equation_solver(equations=[]):
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
    # Solve the system of equations. (Note, we want the answer in parametric form.)
    # Check if determinant is 0
    if np.linalg.det(coefficient_matrix) == 0:
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
    print(ocr_solve("pic.png"))
    return


main()
