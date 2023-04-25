import numpy as np
import re
from OpenCv import ocr

#This function is meant to solve linear systems from an array of linear equations. 
#It will return the solution to the system in parametric form.
#The function will also return the number of solutions to the system, if any.
def equation_solver(equations = []):
    var_regex = r'([-+]?\d*)([a-z])'
    const_regex = r'([-+]?\d+)$'

    #Obtain the number of equations from the array of equations.
    num_equations = len(equations)
    #Obtain the number of variables from the array of equations.
    coeffMatrix = np.zeros((num_equations, num_equations))
    constMatrix = np.zeros((num_equations, 1))
    for i in range(num_equations):
        equation = equations[i]
        #Create a matrix of coefficients from the array of equations.
        matches = re.findall(var_regex, equation)
        coeffs = [int(match[0]) if match[0] else 1 if match[1] else 0 for match in matches]
        coeffs = np.array(coeffs)
        #Create a matrix of constants from the array of equations.
        constant = re.findall(const_regex, equation)
        constants = np.array([int(constant[0])])
        #Add the coefficients to the matrix of coefficients.
        coeffMatrix[i,:] = coeffs
        #Add the constants to the matrix of constants.
        constMatrix[i,:] = constants
    #Solve the system of equations. (Note, we want the answer in parametric form.)
    solution = np.linalg.solve(coeffMatrix, constMatrix)
    return solution

def ocr_solve(file_name):
    img, equations = ocr(file_name)
    solution = equation_solver(equations)
    return solution

def only_eq_solve(equations):
    solution = equation_solver(equations)
    return solution

def main():
    #Test the function.
    # print(equation_solver(["2x + 3y + 4z = 5", "6x + 7y + 8z = 9", "10x + 11y + 12z = 13"]))
    print(ocr_solve("pic.png"))
    return

main()
