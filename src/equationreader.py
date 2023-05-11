import cv2
import pytesseract
import os


# OCR function
def ocr(image_name):

    # Get image path
    path = os.path.dirname(os.path.abspath(__file__))
    image = os.path.join(path, image_name)

    # Load the image
    img = cv2.imread(image)

    # Convert the image to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold the image to make the text more distinct
    img_thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # convert from GRB to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Perform OCR to extract text from the image
    text = pytesseract.image_to_string(img, config='--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789xyz-+=XYZ')

    # Split the text into lines and remove empty lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # Remove any lines that contain only whitespace
    lines = [line for line in lines if line.strip()]

    # turn the lines to lower case
    lines = [line.lower() for line in lines]

    # remove any whitespace in the lines
    lines = [line.replace(' ', '') for line in lines]

    # Display output
    print('OCR detected the following equations:')
    for line in lines:
        print(line)

    # Return the list of equations
    return img, lines

def resize(img = cv2.imread):
    scale = 0.6

    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    dim = (width, height)

    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    return resized

def main():
    # Insert name of image
    image_name = './images/picNS.png'

    # Call the OCR function
    img, text = ocr(image_name)

    # Print the recognized text
    print(text)

if __name__ == '__main__':
    main()
