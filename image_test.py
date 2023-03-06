import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR'

# Input image path
input_image_path = r'D:/CDP/download.jpg'

# Read the input image
img = cv2.imread(input_image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply thresholding to the image
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Perform OCR using pytesseract
text = pytesseract.image_to_string(thresh)

# Print the output
print(text)