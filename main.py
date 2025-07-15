import os
from dotenv import load_dotenv
from google import genai
import sys

# Get connect to google
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():

    if len(sys.argv) != 2:
        print("<Usage> main.py input_str")
        exit(1)

    user_input = sys.argv[1]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=user_input,
    )

    assert response.usage_metadata is not None, "Expected usage metadata"
    print(response.text)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
