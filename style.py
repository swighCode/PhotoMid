BLUE = "#0077be"
BLACK = "#000000"
DARK_GRAY = "#5A5A5A"

FONT = "Calibri"
FONTSIZE = 16

stylesheet = """
    QWidget {
        background-color: #F2F2F2;
        color: %s;
        font-family: "Calibri";
    }
    QLabel {
        color: %s;
        font-size: %spx;
        font-weight: %s;
        font-family: "Calibri";
    }
    QPushButton {
        background-color: %s;
        color: %s;
        border: 2px solid %s;
        border-radius: %spx;
        font-size: %spx;
        font-weight: %s;
        font-family: "Calibri";
    }
""" % (BLACK, DARK_GRAY, FONTSIZE, "normal", BLUE, BLACK, BLUE, 10, FONTSIZE, "normal")