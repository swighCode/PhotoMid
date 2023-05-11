import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from functools import partial
import numpy as np
from OpenCv import ocr
from EquationSolver import matrix_generator,only_eq_solve, plotter_main
from equationtype import manual_equation
from style import stylesheet

# Main GUI class
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PhotoMid'
        self.width = 800
        self.height = 1000
        self.file_name = '' #Starts GUI without an image
        self.equations_list, self.equations_string, self.solution_string, self.coef_matrix, self.const_matrix = list, "", "", None, None
        self.preselected_image = QPixmap(self.file_name)
        self.new_image = None
        self.manual_equation = False
        self.label_image = QLabel(self)
        IMG_SIZE = 750
        self.label_image.setFixedSize(IMG_SIZE, IMG_SIZE)
        self.set_image()
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setStyleSheet(stylesheet)
        self.setGeometry(0, 0, self.width, self.height)
        center_window(self)
        self.create_gui()


    def create_gui(self):
        # Add the labels to a QVBoxLayout
        layout = QVBoxLayout()

        # Display image in GUI, empty if no image selected
        self.set_image()

        # Labels and buttons
        label_input = QLabel("Image, if selected:")
        self.label_equations = QLabel()
        self.input_string = "Equation recognized: \n" + self.equations_string
        self.label_equations.setText(self.input_string)

        # Button for Image selection
        button_image = QPushButton("Choose new image", self)
        button_image.clicked.connect(self.showFileDialog)

        # Button for updating solution
        button_solution = QPushButton("Update solution", self)
        button_solution.clicked.connect(self.on_clicked_solution)

        # Button for plotting solution
        button_plot = QPushButton("Plot solution")
        button_plot.clicked.connect(partial(self.on_clicked_plot))

        # Label for solution
        self.label_solution = QLabel()
        output_string = "Equation solution: \n" + self.solution_string
        self.label_solution.setText(output_string)

        # Create a button and connect it to the showInputDialog function
        user_button = QPushButton("Open input dialog", self)
        user_button.clicked.connect(self.showInputDialog)        

        # displayed object's order in GUI
        layout.addWidget(label_input, alignment=Qt.AlignCenter)
        layout.addWidget(self.label_image, alignment=Qt.AlignCenter)
        layout.setAlignment(self.label_image, Qt.AlignCenter)
        layout.addWidget(button_image, alignment=Qt.AlignCenter)
        layout.addWidget(button_solution, alignment=Qt.AlignCenter)
        layout.addWidget(self.label_equations, alignment=Qt.AlignCenter)
        layout.addWidget(button_plot, alignment=Qt.AlignCenter)
        layout.addWidget(user_button)
        layout.addWidget(self.label_solution, alignment=Qt.AlignCenter)

        # Set the layout on the application's window
        self.setLayout(layout)

    # Update the GUI image
    def set_image(self):
        if self.new_image is not None:
            self.label_image.setPixmap(self.new_image.scaled(self.label_image.width(), self.label_image.height(), Qt.KeepAspectRatio))
        elif self.preselected_image is not None:
            self.label_image.setPixmap(self.preselected_image.scaled(self.label_image.width(), self.label_image.height(), Qt.KeepAspectRatio))
        else:
            self.label_image.clear()

    # Function for retrieving solution from solver
    def solve_equation(self):
        _, equations = ocr(self.file_name)
        equations_string = "\n".join(equations)

        solution = only_eq_solve(equations)
        coef_matrix, const_matrix = matrix_generator(equations)

        # solution_string can come either as a string or as np.array
        if isinstance(solution, str):
            solution_string = solution
        else:
            solution_string = np.array2string(solution, separator=' ')
        return equations_string, solution_string, coef_matrix, const_matrix
    
    # Function for solving and updating solution variables for manual input
    def solve_equation_with_list(self, equations_string: str, equations_list: list):
        solution = only_eq_solve(equations_list)
        coef_matrix, const_matrix = matrix_generator(equations_list)
        solution_string = np.array2string(solution, separator=' ')
        self.equations_string, self.solution_string, self.coef_matrix, self.const_matrix = equations_string, solution_string, coef_matrix, const_matrix
        self.equations_list = equations_list
    
    # Function for updating solution variables
    def set_solutions(self):
        self.equations_string, self.solution_string, self.coef_matrix, self.const_matrix = self.solve_equation()
        self.equations_list = self.equations_string.split("\n")

    # Function for button updating solution
    def on_clicked_solution(self):
        if self.new_image is None and self.manual_equation is False:
            print("No image selected / manual input")
            if not os.path.exists(self.file_name):
                print("File not found")
                return
            return
        if self.manual_equation is True:
            self.manual_equation = False # reset it.
        else:
            self.set_solutions()
        self.label_equations.setText("Equation recognized: \n" + self.equations_string)
        self.label_solution.setText("Equation solution: \n" + self.solution_string)

    # Function for button plotting solution
    def on_clicked_plot(self):
        if self.manual_equation is False: # Check whether there is an ongoing manual input
            self.set_solutions
        if self.coef_matrix is None or self.const_matrix is None:
            print("Nothing to plot")
            return
        plotter_main(self.equations_list)
        print("Plotting")

    # Function for opening input dialog
    def showInputDialog(self):
        # Create an instance of the InputDialog and show it as a modal dialog
        dialog = InputDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Get the text entered by the user and save it
            text = dialog.text()
            # Do something with the text, e.g. save it to a file or print it
            print("User entered:", text)
            equation_as_list = manual_equation(text)
            self.solve_equation_with_list(text, equation_as_list)
            self.manual_equation = True

    # Function for opening file dialog
    def showFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "All Files (*);;Image Files (*.png *.jpg *.jpeg *.pdf)", options=options)
        if fileName:
            # Update the new image
            self.new_image = QPixmap(fileName)
            # Update the GUI image
            self.set_image()
            # Update the file name
            self.set_file_name(fileName)

    # Function for updating image name
    def set_file_name(self, file_name):
        self.file_name = file_name


# Class for logic of input from user 
class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Window settings
        self.setWindowTitle("Enter equation / equations")
        self.setGeometry(0, 0, 300, 50)
        center_window(self)
        
        # Create a layout for the dialog
        layout = QVBoxLayout(self)
        
        # Add a line edit widget for text input
        self.text_edit = QLineEdit(self)
        layout.addWidget(self.text_edit)
        
        # Add a dialog button box with OK and Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def text(self):
        return self.text_edit.text()


# Function for resizing image
def resize(img: QPixmap) -> QPixmap:
    width, height = 200, 200
    scaled_img = img.scaled(width, height, aspectRatioMode=Qt.IgnoreAspectRatio, transformMode=Qt.FastTransformation)
    return scaled_img

# Manipulate GUI settings
def app_settings(app: QApplication([])):
    app.setWindowIcon(QIcon("./app_images/logo3"))

# Centers the window on user's screen
def center_window(self):
    # Get the geometry of the screen
    screen = QDesktopWidget().screenGeometry()
            
    # Get the geometry of the main window
    window = self.geometry()
            
    # Calculate the center point of the screen
    center_point = screen.center()
            
    # Move the main window to the center of the screen
    window.moveCenter(center_point)
    self.setGeometry(window)

if __name__ == '__main__':
    app = QApplication([])
    app_settings(app)
    window = App()
    window.show()
    app.exec_()