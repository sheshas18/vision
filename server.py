import subprocess
import cv2
import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Define a temporary directory to store uploaded images
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Route to serve the index.html file
@app.route("/")
def index():
    return render_template("index.html")  # Serves index.html from the templates folder
@app.route("/main.html")
def login():
    return render_template("main.html")
@app.route("/scribble.html")
def scribble():
    return render_template("scribble.html")
@app.route("/texttospeech.html")
def texttospeech():
    return render_template("texttospeech.html")
@app.route("/speechtotext.html")
def speechtotext():
    return render_template("speechtotext.html")
@app.route("/process-image", methods=["POST"])
def process_image():
    # Check if a file is uploaded
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, "screenshot_image.png")  # Save to the uploads folder
    file.save(file_path)

    print(f"Image saved at: {file_path}")  # Debug line

    # Load and preprocess image
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return jsonify({"error": "Image not loaded correctly"}), 400
    print("Image loaded successfully")  # Debug line

    try:
        # Run test.py script
        result = subprocess.run(["python3", "test.py"], capture_output=True, text=True)
        print(f"test.py output: {result.stdout}")  # Debug line

        # Check if the subprocess ran successfully
        if result.returncode != 0:
            return jsonify({"error": f"Error in test.py: {result.stderr}"}), 500

        # Store the result in a text file (optional)
        with open(os.path.join(UPLOAD_FOLDER, "recognized_text.txt"), "w") as f:
            f.write(result.stdout)

        # Return the recognized text
        return jsonify({"message": result.stdout.strip()})  # Match frontend's expected field

    except Exception as e:
        print(f"Error: {e}")  # Debug line
        return jsonify({"error": str(e)}), 500

    finally:
        # Clean up: Delete the temporary image file
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted temporary file: {file_path}")  # Debug line

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
