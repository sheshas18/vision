import os
from google import genai
from google.genai import types
import PIL.Image

# Define the directory and file name
UPLOAD_FOLDER = "uploads"
image_file = "screenshot_image.png"

# Dynamically create the full path to the image
image_path = os.path.join(UPLOAD_FOLDER, image_file)

# Load the image using the dynamic path
image = PIL.Image.open(image_path)

# Initialize Google genAI client with your API key
client = genai.Client(api_key="AIzaSyDa_LIylvC_6sL7PH1YFQKLIxNf_95h4l0")

# Send the image to the model and get a response
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["What is this image?", image])

# Print the response text
print(response.text)