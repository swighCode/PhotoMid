import csv

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
    with open(CSV_FILE_PATH, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader]
    rows[0][f'Equation{equation_index}'] = new_equation
    equations_list = ','.join([rows[0][f'Equation{i}'] for i in range(1, 4)])
    rows[0]['EquationsList'] = equations_list
    with open(CSV_FILE_PATH, 'w', newline='') as csvfile:
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

################################################################################

test_equation = "1x+3y+2z=1 -1x+1y+1z=2 -1x+1y+2z=3"
MATRIX_SIZE = 3

# Select which method to use for updating csv file
def select_equation_type(equation: str):
    if " " in equation:
        equations = equation.split()
        if len(equations) != MATRIX_SIZE:
            print("Error, cannot find three equations, equations found: %d" % len(equations))
            return
        whitespace_type()
        return
    string_type(equation)

# Updating csv file for multiple strings format
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
    if not exists:
        for col in CSV_HEADERS:
            if not any(row[col] for row in rows):
                rows[0][col] = equation
                update_equation(1, equation)
                break

    # # If equation doesn't exist, append it to the next column
    # if not exists:
    #     update_equation(int(next_column) + 1, equation)

# Updating csv file for whitespace equation format
def whitespace_type(equation: str):
    equations = equation.split()
    for i in range(len(equations)):
        update_equation(i+1, equations[i])


# main function
def main():
    write_initial_data()
    #update_equation(1, "hejpadig")
    # test_equation = "1x+3y+2z=1 -1x+1y+1z=2 -1x+1y+2z=3"
    # whitespace_type(test_equation)
    eq1 = "1x+3y+2z=1"
    eq2 = "-1x+1y+1z=2" 
    eq3 = "-1x+1y+2z=3"
    string_type(eq1)
    string_type(eq2)
    string_type(eq3)

if __name__ == "__main__":
    main()
