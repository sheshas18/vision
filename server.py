import subprocess
import pytesseract
from PIL import Image
import cv2
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/process-image", methods=["POST"])
def process_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_path = "screenshot_image.png"
    file.save(file_path)

    print(f"Image saved at: {file_path}")  # Debug line

    # Load and preprocess image
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return jsonify({"error": "Image not loaded correctly"}), 400
    print(f"Image loaded successfully")

    # Run compare.py
    result = subprocess.run(["python3", "compare.py"], capture_output=True, text=True)
    print(f"compare.py output: {result.stdout}")  # Debug line

    # Store the result in a text file
    with open("recognized_text.txt", "w") as f:
        f.write(result.stdout)

    # Return the recognized text
    return jsonify({"text": result.stdout})

if __name__ == "__main__":
    app.run(debug=True)
