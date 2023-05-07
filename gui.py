import os
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLabel, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from functools import partial
import numpy as np
from OpenCv import ocr
from EquationSolver import matrix_generator,only_eq_solve, plotter

# Main GUI class
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PhotoMid'
        self.left = 800
        self.top = 200
        self.width = 1000
        self.height = 800
        self.file_name = "pic.png"
        self.preselected_image = QPixmap(self.file_name)
        self.new_image = None
        self.label_image = QLabel(self)
        self.label_image.setFixedSize(1000, 500)
        self.set_image()
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.create_gui()


    def create_gui(self):
        # Add the labels to a QVBoxLayout
        layout = QVBoxLayout()

        # Display image in GUI, empty if no image selected
        self.set_image()

        # Retrieve and update solution
        equations_string, solution_string, coef_matrix, const_matrix = self.solve_equation()

        # Labels and buttons
        label_input = QLabel("Image, if selected:")
        self.label_equations = QLabel()
        self.input_string = "Equation recognized: \n" + equations_string
        self.label_equations.setText(self.input_string)

        # Button for Image selection
        button_image = QPushButton("Choose new image", self)
        button_image.clicked.connect(self.showFileDialog)

        # Button for updating solution
        button_solution = QPushButton("Update solution", self)
        button_solution.clicked.connect(self.on_clicked_solution)

        # Button for plotting solution
        button_plot = QPushButton("plot solution")
        button_plot.clicked.connect(partial(self.on_clicked_plot, coef_matrix, const_matrix))

        # Label for solution
        label_output = QLabel()
        output_string = "Equation solution: \n" + solution_string
        label_output.setText(output_string)

        # Create a button and connect it to the showInputDialog function
        user_button = QPushButton("Open input dialog", self)
        user_button.clicked.connect(self.showInputDialog)        

        # displayed object's order in GUI
        layout.addWidget(label_input, alignment=Qt.AlignCenter)
        layout.addWidget(self.label_image, alignment=Qt.AlignCenter)
        layout.addWidget(button_image, alignment=Qt.AlignCenter)
        layout.addWidget(button_solution, alignment=Qt.AlignCenter)
        layout.addWidget(self.label_equations, alignment=Qt.AlignCenter)
        layout.addWidget(button_plot, alignment=Qt.AlignCenter)
        layout.addWidget(user_button)
        layout.addWidget(label_output, alignment=Qt.AlignCenter)

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
        solution_string = np.array2string(solution, separator=' ')
        return equations_string, solution_string, coef_matrix, const_matrix
    
    # Function for button updating solution
    def on_clicked_solution(self):
        if self.new_image is None:
            print("No image selected")
            return
        if not os.path.exists(self.file_name):
            print("File not found")
            return
        equations_string, solution_string, coef_matrix, const_matrix = self.solve_equation()
        self.label_equations.setText("Equation recognized: \n" + equations_string)
        self.label_equations.repaint()
        #self.create_gui()

    # Function for button plotting solution
    def on_clicked_plot(self, coef_matrix, const_matrix):
        plotter(coef_matrix, const_matrix)
        print("confirmation")

    # Function for opening input dialog
    def showInputDialog(self):
        # Create an instance of the InputDialog and show it as a modal dialog
        dialog = InputDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Get the text entered by the user and save it
            text = dialog.text()
            # Do something with the text, e.g. save it to a file or print it
            print("User entered:", text)

    def showFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "All Files (*);;Image Files (*.png *.jpg *.jpeg *.pdf)", options=options)
        if fileName:
            # Update the new image
            self.new_image = QPixmap(fileName)
            # Update the GUI image
            self.set_image()


# Class for logic of input from user 
class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Enter text")
        
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


if __name__ == '__main__':
    app = QApplication([])
    window = App()
    window.show()
    app.exec_()