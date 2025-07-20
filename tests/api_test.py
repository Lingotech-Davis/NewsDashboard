from google import genai
from google.genai import types
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def ask_gemini(prompt, content, test_mode=False):
    if test_mode:
        return "In test mode, will not call API"
    client = genai.Client(api_key=GEMINI_API_KEY)

    contents = prompt + content

    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        config=types.GenerateContentConfig(
            system_instruction="You don't know anything except the information provided for you. Base your answer solely off of this information provided."
        ),
        contents=contents
    )
    
    return response.text