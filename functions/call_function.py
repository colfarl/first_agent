from functions.write_file import write_file
from functions.run_python import run_python_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from config import WORKING_DIRECTORY
from google.genai import types

def call_function(function_call_part, verbose=False):

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_dict = {
        'write_file': write_file, 
        'run_python_file': run_python_file, 
        'get_files_info': get_files_info, 
        'get_file_content': get_file_content
    }
    
    function_name = function_call_part.name
    args = function_call_part.args

    if function_name not in function_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    else:
        try:
            function_result = function_dict[function_name](WORKING_DIRECTORY,**args)
            return types.Content(
                        role="tool",
                        parts=[
                            types.Part.from_function_response(
                                name=function_name,
                                response={"result": function_result},
                            )
                        ],
                    )
        except:
            return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_name,
                            response={"error": f"Unknown function: {function_name}"},
                        )
                    ],
                )

