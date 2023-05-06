from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLabel, QVBoxLayout
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
        self.top = 500
        self.width = 800
        self.height = 500
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.create_gui()

    def create_gui(self):

        file_name = "pic.png"

        img, equations = ocr(file_name)
        equations_string = "\n".join(equations)

        solution = only_eq_solve(equations)
        coef_matrix, const_matrix = matrix_generator(equations)
        solution_string = np.array2string(solution, separator=' ')

        # Add the labels to a QVBoxLayout
        layout = QVBoxLayout()

        # displayed objects in GUI
        image = QPixmap(file_name)
        image = resize(image)
        label_image = QLabel()
        label_image.setPixmap(image)
        label_input = QLabel("Image input:")
        label_r_input = QLabel()
        input_string = "Equation recognized: \n" + equations_string
        label_r_input.setText(input_string)
        button_plot = QPushButton("plot solution")
        button_plot.clicked.connect(partial(self.on_clicked_plot, coef_matrix, const_matrix))
        label_output = QLabel()
        output_string = "Equation solution: \n" + solution_string
        label_output.setText(output_string)

        # Create a button and connect it to the showInputDialog function
        user_button = QPushButton("Open input dialog", self)
        user_button.clicked.connect(self.showInputDialog)        

        # displayed object's order in GUI
        layout.addWidget(label_input, alignment=Qt.AlignCenter)
        layout.addWidget(label_image, alignment=Qt.AlignCenter)
        layout.addWidget(label_r_input, alignment=Qt.AlignCenter)
        layout.addWidget(button_plot, alignment=Qt.AlignCenter)
        layout.addWidget(user_button)
        layout.addWidget(label_output, alignment=Qt.AlignCenter)

        self.setLayout(layout)

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