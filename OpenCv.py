
import cv2
import pytesseract
import numpy as np
import os
import cv2
import pytesseract
import numpy as np
import os
#OCR function
def ocr(image_path):
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\bowst\\kth\\inda\\Private\\Tesser\\Tesseract-OCR\\tesseract.exe'
    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold the image to make the text more distinct
    thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Perform OCR to extract text from the image
    text = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')

    # Split the text into lines and remove empty lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # Prompt the user to confirm the detected equations
    print('OCR detected the following equations:')
    for line in lines:
        print(line)
    confirm = input('Is this correct? (Y/N) ').strip().lower() == 'y'

    # If the detected equations are not correct, prompt the user to input them manually
    if not confirm:
        lines = []
        num_equations = int(input('How many equations do you want to input? '))
        for i in range(num_equations):
            line = input(f'Enter equation {i + 1}: ')
            lines.append(line)

    # Return the list of equations
    return lines


#Main function
def main():
    #Get the path of the image
    path = os.path.dirname(os.path.abspath(__file__))
    image = os.path.join(path, 'pic2.png')

    #Call the OCR function
    text = ocr(image)

    #Print the recognized text
    print(text)

if __name__ == '__main__':
    main()
