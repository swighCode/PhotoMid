import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\bowst\\kth\\inda\\Private\\Tesser\\Tesseract-OCR\\tesseract.exe'

# Load the image
img = cv2.imread("C:\\Users\\bowst\\kth\\inda\\Private\\Tesser\\pic2.png")

# Convert the image to grayscale
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Threshold the image to make the handwriting more distinct
thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Find contours of handwriting regions in the image
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Loop through each contour and extract the handwriting region
for contour in contours:
    # Get the bounding box of the contour
    x, y, w, h = cv2.boundingRect(contour)

    # Extract the handwriting region
    handwriting_region = thresh[y:y+h, x:x+w]

    # Apply OCR to recognize the text in the handwriting region
    text = pytesseract.image_to_string(handwriting_region)

    text = text.replace("\n", " ")

    # Print the recognized text

    # Print the recognized text without whitespace characters

print (text)