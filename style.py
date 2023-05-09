BLUE = "#0077be"
LIGHT_GRAY = "#e6e6e6"
DARK_GRAY = "#333333"

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
""" % (LIGHT_GRAY, DARK_GRAY, FONTSIZE, "normal", BLUE, LIGHT_GRAY, BLUE, 10, FONTSIZE, "normal")