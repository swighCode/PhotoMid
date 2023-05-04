import os
from fractions import Fraction
import copy

# turn string into list
def string_to_list(text: str) -> list:
    equations = text.split(" ")
    return equations

# check if input is empty
def check_input(input_list: list):
    if input_list.count == 0:
        print("no input detected")
        os.close
    else:
        print("input detected: " + " ".join(input_list))
        return input_list

# turn list into matrix
def list_to_matrix(input_list: list) -> list:
    equations = []
    for equations_xyz in input_list:
        chars = [*equations_xyz]
        i = 0
        constant = ''
        for char in chars:
            if char.startswith('x'):
                # break here
                if chars[i - 1].startswith(' '):
                    constant = '1'
                constant = constant + ' '
            elif char.startswith('y'):
                # break here
                if chars[i - 1].startswith(' '):
                    constant = '1'
                constant = constant + ' '
            elif char.startswith('z'):
                # break here
                if chars[i - 1].startswith(' '):
                    constant = '1'
                constant = constant + ' '
            elif char.startswith('+'):
                # break here
                if chars[i - 1].startswith(' '):
                    constant = '1'
                constant = constant
            elif char.startswith('='):
                # break here
                if chars[i - 1].startswith(' '):
                    constant = '1'
                constant = constant
            else:
                constant = constant + char 
            i = i + 1
        # turn string into array matrix
        const_list = constant.split(' ')
        equations.append(const_list)
    # Convert the matrix elements to floating-point numbers
    for i in range(len(equations)):
        for j in range(len(equations[i])):
            equations[i][j] = float(equations[i][j])
    return equations

# turn input into matrix
def input_to_matrix(text: str) -> list:
    if isinstance(text, list):
        input_list = text
    elif isinstance(text, str):
        input_list = string_to_list(text)
    else:
        raise TypeError("Input must be a string or a list")
    check_input(input_list)
    equations = list_to_matrix(input_list)
    return equations

# turn matrix into augmented matrix with only coefficients
def matrix_to_coefficients(matrix: list) -> list:
    augmented = []
    for equation in matrix:
        augmented.append(equation[:-1])
    return augmented

# turn matrix into augmented matrix with only solutions
def matrix_to_solutions(matrix: list) -> list:
    solutions = []
    for equation in matrix:
        solutions.append(equation[-1])
    return solutions

# find inverse of coefficient matrix
def inverse_coefficient(matrix: list) -> list:
    # Create an identity matrix of the same size as the input matrix
    identity = [[Fraction(int(i==j),1) for j in range(len(matrix))] for i in range(len(matrix))]

    # Make a copy of the input matrix, so that we don't modify the original
    A = copy.deepcopy(matrix)

    # Apply Gaussian elimination to the input matrix to convert it to an upper triangular matrix
    for i in range(len(A)):
        pivot = A[i][i]
        if pivot == 0:
            raise ValueError("Matrix is singular and has no inverse.")
        for j in range(len(A)):
            A[i][j] /= pivot
            identity[i][j] /= pivot
        for k in range(i+1, len(A)):
            factor = A[k][i]
            for j in range(len(A)):
                A[k][j] -= factor * A[i][j]
                identity[k][j] -= factor * identity[i][j]

    # Apply back-substitution to the upper triangular matrix to get the inverse
    for i in reversed(range(len(A))):
        for k in reversed(range(i)):
            factor = A[k][i]
            for j in range(len(A)):
                A[k][j] -= factor * A[i][j]
                identity[k][j] -= factor * identity[i][j]
    # return inverse
    return identity

# solve augmented matrix with solution matrix
def solve_augmented(inverse: list, solutions: list) -> list:
    # solve matrix by multiplying inverse matrix with solution matrix
    solution = []
    for i in range(len(inverse)):
        solution.append(sum([inverse[i][j] * solutions[j] for j in range(len(inverse))]))

    # return solution
    return solution

# main function
def main():
    # testing manual input
    # text = '2x+3y+4z=5 6x+7y+8z=9 10x+11y+12z=13'
    text = '1x+1y+1z=1 2x+1y+1z=2 1x+1y+2z=2'
    matrix = input_to_matrix(text)
    print(matrix)
    coefficient_matrix = matrix_to_coefficients(matrix)
    print(coefficient_matrix)
    solutions_matrix = matrix_to_solutions(matrix)
    print(solutions_matrix)
    inverse_matrix = inverse_coefficient(coefficient_matrix)
    print(inverse_matrix)
    solution = solve_augmented(inverse_matrix, solutions_matrix)
    print(solution)
    

if __name__ == "__main__":
    main()
