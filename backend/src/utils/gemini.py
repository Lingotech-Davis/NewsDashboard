"""requirements.txt
google-genai
"""

from google import genai
from google.genai import types


def ask_gemini(prompt, content, instruction, GEMINI_API_KEY, test_mode=False):
    if test_mode:
        return "In test mode, will not call API"
    client = genai.Client(api_key=GEMINI_API_KEY)

    contents = (
        prompt + content + prompt
    )  # Putting prompt before and after context so it is not ignored

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=instruction),
        contents=contents,
    )

    return response.text


def read_with_gemini(top_n_chunks, GEMINI_API_KEY):
    """
    feed the chunks, a prompt, and system instructions into gemini
    """

    # turn the list of chunks into a string
    sep = ".\n"
    content = sep.join(top_n_chunks)

    instructions = "You don't know anything except the information provided for you. Base your answer solely off of this information provided."
    prompt = "Evaluate the validity of the users question, or generate an accurate summary from the information provided."

    gemini_response = ask_gemini(
        prompt, content, instructions, GEMINI_API_KEY, test_mode=False
    )

    return gemini_response
