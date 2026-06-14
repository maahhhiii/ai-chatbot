from google import genai
from config import GEMINI_API_KEY

# Create Gemini client
client = genai.Client(
    api_key=GEMINI_API_KEY
)


def get_ai_response(prompt):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text