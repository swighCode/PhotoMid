from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import numpy as np
from OpenCv import ocr
from EquationSolver import only_eq_solve


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PhotoMid'
        self.left = 50
        self.top = 50
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
        solution_string = np.array2string(solution, separator=' ')

        # Add the labels to a QVBoxLayout
        layout = QVBoxLayout()

        # displayed objects in GUI
        image = QPixmap(file_name)
        label_image = QLabel()
        label_image.setPixmap(image)
        label_input = QLabel("Image input:")
        label_r_input = QLabel()
        input_string = "Equation recognized: \n" + equations_string
        label_r_input.setText(input_string)
        button_y = QPushButton("I recognize this image")
        button_y.clicked.connect(self.on_clicked_y)
        button_n = QPushButton("I do NOT recognize this image")
        button_n.clicked.connect(self.on_clicked_n)
        label_output = QLabel()
        output_string = "Equation solution: \n" + solution_string
        label_output.setText(output_string)
        textbox = QTextEdit()

        # displayed object's order in GUI
        layout.addWidget(label_input)
        layout.addWidget(label_image)
        layout.addWidget(label_r_input)
        layout.addWidget(button_y)
        layout.addWidget(button_n)
        layout.addWidget(textbox)
        layout.addWidget(label_output)

        self.setLayout(layout)


    def on_clicked_y(self):
        print("confirmation")

    def on_clicked_n(self):
        print("Wrong input")


if __name__ == '__main__':
    app = QApplication([])
    window = App()
    window.show()
    app.exec_()