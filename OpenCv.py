import cv2
import pytesseract
import os


# OCR function
def ocr(image_name):
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'

    # Get image path
    path = os.path.dirname(os.path.abspath(__file__))
    image = os.path.join(path, image_name)

    # Load the image
    img = cv2.imread(image)

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
    confirm = input('Is this correct? (y/n) ').strip().lower()

    # If the detected equations are not correct, prompt the user to input them manually
    if not confirm:
        lines = []
        num_equations = int(input('How many equations do you want to input? '))
        for i in range(num_equations):
            line = input(f'Enter equation {i + 1}: ')
            lines.append(line)

    # Return the list of equations
    return img, lines


# Main function
def main():
    # Insert name of image
    image_name = 'pic.png'

    # Call the OCR function
    img, text = ocr(image_name)

    # Print the recognized text
    print(text)

if __name__ == '__main__':
    main()
