import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import SYSTEM_PROMPT
from functions.get_files_info import schema_get_files_info


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
    
    # Configure LLM 
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=SYSTEM_PROMPT
        )
    )

    assert response.usage_metadata is not None, "Expected usage metadata"
        
    if is_verbose:
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    function_calls = response.function_calls
    
    if function_calls is not None and len(function_calls) > 0:
        for function_call_part in function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(response.text)

if __name__ == "__main__":
    main()
