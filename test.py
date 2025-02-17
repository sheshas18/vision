from google import genai
from google.genai import types

import PIL.Image

image = PIL.Image.open('screenshot_image.png')

client = genai.Client(api_key="AIzaSyDa_LIylvC_6sL7PH1YFQKLIxNf_95h4l0")
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["What is this image?", image])

print(response.text)