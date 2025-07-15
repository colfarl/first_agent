import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

# Get connect to google
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("ERROR: API not present in .env file")
    exit(1)

client = genai.Client(api_key=api_key)

def main():
    #Set up argument parser
    parser = argparse.ArgumentParser(
        description= "CLI for basic agent"
    )
    parser.add_argument(
        "input_str",
        help="User prompt to send to LLM"
    )
    parser.add_argument(
            "--verbose",
            "-v",
            action="store_true",
            help="Print additional API usage info"
    )

    args = parser.parse_args()
    user_prompt = args.input_str
    is_verbose = args.verbose
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    assert response.usage_metadata is not None, "Expected usage metadata"
    print(response.text)
    if is_verbose:
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()
