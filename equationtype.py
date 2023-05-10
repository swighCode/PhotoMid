import csv

# Define the CSV file path and the column headers
CSV_FILE_PATH = 'equations.csv'
CSV_HEADERS = ['Equation1', 'Equation2', 'Equation3', 'EquationsList']

# Function to write the initial data to the CSV file
def write_initial_data():
    with open(CSV_FILE_PATH, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerow({'Equation1': "", 'Equation2': "", 'Equation3': "", 'EquationsList': []})

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
    # Load the CSV file
    with open('equations.csv', 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    # Determine the next column index to update
    last_column = data[0][0]
    next_column = str((int(last_column) + 1) % 3)
    data[0][0] = next_column

    # Check if equation is already in the CSV file
    exists = False
    for i in range(1, 4):
        if equation == data[i][next_column]:
            exists = True
            break

    # If equation doesn't exist, append it to the next column
    if not exists:
        if len(data[next_column + 1]) < 3:
            data[next_column + 1].append(equation)
        else:
            data[next_column + 1][0] = equation

    # Write the updated data back to the CSV file
    with open('equations.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)


# Updating csv file for whitespace equation format
def whitespace_type(equation: str):
    equations = equation.split()
    # Try parsing equations as three separate strings
    try:
        eq1, eq2, eq3 = " ".join(equations).split(" ")
    except ValueError:
        # If parsing fails, assume equations is a list of three strings
        eq1, eq2, eq3 = equations
    for i in range(len(equations)):
        update_equation(i, equations[i])


# main function
def main():
    write_initial_data()
    test_equation = "1x+3y+2z=1 -1x+1y+1z=2 -1x+1y+2z=3"
    eq1 = "1x+3y+2z=1"
    eq2 = "-1x+1y+1z=2" 
    eq3 = "-1x+1y+2z=3"
    update_equation(1, "hejpadig")
    whitespace_type(test_equation)
    # string_type(eq1)
    # string_type(eq2)
    # string_type(eq3)

if __name__ == "__main__":
    main()
