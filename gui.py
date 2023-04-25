from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from OpenCv import ocr


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
        img, equations = ocr("pic2.png")
        equations_string = " ".join(equations)

        # Add the labels to a QVBoxLayout
        layout = QVBoxLayout()

        # displayed objects in GUI
        image = QPixmap("pic2.png")
        label_image = QLabel()
        label_image.setPixmap(image)
        label_input = QLabel("Image input:")
        label_r_input = QLabel()
        label_r_input.setText(equations_string)
        button_y = QPushButton("I recognize this image")
        button_y.clicked.connect(self.on_clicked_y)
        button_n = QPushButton("I do NOT recognize this image")
        button_n.clicked.connect(self.on_clicked_n)
        label_output = QLabel("Answer output:")
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