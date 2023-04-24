import numpy as np
import math as m
import re
import OpenCv

#This function is meant to solve linear systems from an array of linear equations. 
#It will return the solution to the system in parametric form.
#The function will also return the number of solutions to the system, if any.
def equation_solver(equations = []):
    regex = r'([-+]?\d*)[a-z]?'
    #Obtain the number of equations from the array of equations.
    num_equations = len(equations[0])
    #Obtain the number of variables from the array of equations.
    coeffMatrix = np.empty((num_equations, num_equations))
    constMatrix = np.empty((num_equations, 1))
    for i in range(num_equations):
        equation1 = equations[0]
        equation2 = equation1[i]
        #Following line is unnecessary (?), but I'm keeping it here for now.
        #if equation[i] == 'x' or equation[i] == 'y' or equation[i] == 'z':
            #num_variables = i
        #Create a matrix of coefficients from the array of equations.
        matches = re.findall(regex, equation2)
        coeffs = [int(matches[i]) if matches[i].isdigit() else 1 for i in range(len(matches)-1)]
        coeffs = np.array(coeffs)
        #Create a matrix of constants from the array of equations.
        constant = [int(matches[-1]) if matches[-1].isdigit() else 0]
        constants = np.array(constant)
        #Add the coefficients and to the matrix of coefficients.
        np.vstack(coeffMatrix, coeffs)
        #Add the constants to the matrix of constants.
        np.vstack(constMatrix, constants)
    #Solve the system of equations. (Note, we want the answer in parametric form.)
    solution = np.linalg.inv(coeffMatrix).dot(constMatrix)
    return solution

def main():
    #Test the function.
    print(equation_solver(["2x+3y+4z=5", "6x+7y+8z=9", "10x+11y+12z=13"]))
    return 0

if __name__ == "__main__":
    main()