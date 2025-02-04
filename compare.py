import pytesseract
from PIL import Image
import cv2

# Check if image is being loaded correctly
image_path = "screenshot_image.png"
print(f"Loading image from {image_path}")
image = cv2.imread(image_path)

if image is None:
    print("Failed to load image.")
else:
    print("Image loaded successfully.")

# Preprocess the image (thresholding)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Convert to PIL Image
pil_image = Image.fromarray(thresh_image)

# Extract text using pytesseract
text = pytesseract.image_to_string(pil_image, config="--oem 3 --psm 6")

print(f"Extracted text: {text}")

# You can also return the text back to the Flask server if needed
