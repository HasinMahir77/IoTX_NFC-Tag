import easyocr
import cv2

# Initialize reader (English)
reader = easyocr.Reader(['en'])

# Read text from image
text = reader.readtext('guitar1.jpg', detail=0)  # detail=0 for plain text

print("Extracted Text:")
print("\n".join(text))