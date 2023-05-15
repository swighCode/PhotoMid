import csv

# I want to highlight that the first four function for initilazing, reading and writing to the csv file is mainly written by ChatGPT as 
# we have had no experience of working with this format before.

# Define the CSV file path and the column headers
CSV_FILE_PATH = 'equations.csv'
CSV_HEADERS = ['Equation1', 'Equation2', 'Equation3', 'EquationsList']

# Function to write the initial data to the CSV file
def write_initial_data():
    with open(CSV_FILE_PATH, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerow({'Equation1': "", 'Equation2': "", 'Equation3': "", 'EquationsList': ""})

# Function to update an equation in the CSV file
def update_equation(equation_index, new_equation):
    with open(CSV_FILE_PATH, 'r', newline='') as csvfile: # read mode
        reader = csv.DictReader(csvfile) # dictonary with column header as key and equation as value.
        rows = [row for row in reader]
    rows[0][f'Equation{equation_index}'] = new_equation
    equations_list = ','.join([rows[0][f'Equation{i}'] for i in range(1, 4)])
    rows[0]['EquationsList'] = equations_list
    with open(CSV_FILE_PATH, 'w', newline='') as csvfile: # write mode
        writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerow(rows[0])

# Function to retrieve the list of equations from the CSV file
def get_equations_list():
    with open(CSV_FILE_PATH, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader]
    equations_list = rows[0]['EquationsList']
    return equations_list.split(',')

# GUI uses this function to get the corresponding equation list
def manual_equation(text: str) -> list:
    text = text.lower
    text = text.replace(",", ".") # prevent user from ruining the csv file
    select_equation_type(text)
    equations_as_list = get_equations_list()
    return equations_as_list

MATRIX_NUM = 3

# Select which method to use for updating csv file
def select_equation_type(equation: str):
    if " " in equation:
        equations = equation.split()
        if len(equations) != MATRIX_NUM:
            print("Error, cannot find three equations, equations found: %d" % len(equations))
            return
        whitespace_type(equation)
        return
    string_type(equation) # NOT WORKING!!!

# Updating csv file for multiple strings format
# The idea is that the user inputs one euqtion at the time and the program keeps track of which euqtions have been update and which should be replaced.
# Have not come up with a good enough idea to implement this though.
# DOES NOT WORK!!!!
def string_type(equation: str):
    with open(CSV_FILE_PATH, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader]

    # Check if equation is already in the CSV file
    exists = False
    for row in rows:
        for col in CSV_HEADERS:
            if equation == row[col]:
                exists = True
                break
    # If equation doesn't exist, append it to the first available column
    # Keep track of what the last used column was then use update_equation()


# Updating csv file for whitespace equation format
def whitespace_type(equation: str):
    equations = equation.split()
    for i in range(len(equations)):
        update_equation(i+1, equations[i]) #column index begins from 1

# main function
def main():
    write_initial_data()
    #update_equation(1, "hejpadig")
    test_equation = "1x+3y+2z=1 -1x+1y+1z=2 -1x+1y+2z=3"
    equation_list =  manual_equation(test_equation)
    print(equation_list)
    # whitespace_type(test_equation)
    #eq1 = "1x+3y+2z=1"
    #eq2 = "-1x+1y+1z=2" 
    #eq3 = "-1x+1y+2z=3"
    #string_type(eq1)
    #string_type(eq2)
    #string_type(eq3)

if __name__ == "__main__":
    main()
