import os
from config import MAX_CHARS
from google.genai import types

# Define functions to make them LLM readable
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="read contents of file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to the file we want to read, relative to the working directory.",
            ),
        },
    ),
)



def get_file_content(working_directory, file_path):
    
    full_path = os.path.join(working_directory, file_path or "")
    abs_full  = os.path.abspath(full_path)
    abs_work  = os.path.abspath(working_directory)

    if not abs_full.startswith(abs_work):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_full):
        return f'Error: File not found or is not a regular file: "{file_path}"'
     
    with open(abs_full, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        if len(file_content_string) == MAX_CHARS:
            file_content_string +=  f' "{file_path}" truncated at {MAX_CHARS} characters'

        return file_content_string

