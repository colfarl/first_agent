import os
import subprocess
from google.genai import types


# Define functions to make them LLM readable
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="run python file with optional additional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to the file we want to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="add command line arguments, if not provided program will run as 'python file_path'",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="each argument passed to the script"
                )
            ),
        },
    ),
)



def run_python_file(working_directory, file_path, args=[]):
      
    full_path = os.path.join(working_directory, file_path or "")
    abs_full  = os.path.abspath(full_path)
    abs_work  = os.path.abspath(working_directory)

    if not abs_full.startswith(abs_work):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_full): 
        return f'Error: File "{file_path}" not found.' 
    
    if not abs_full.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    file_run = ['python', abs_full]
    if len(args) > 0:
        file_run.extend(args)

    try:
        result = subprocess.run(file_run, capture_output=True, timeout=30, cwd=abs_work, text=True)
        code = result.returncode
        out = str(result.stdout)
        err = str(result.stderr)
        if code != 0:
            return f'Error: Process exited with code {code}'
        if len(out) == 0 and len(err) == 0:
            return 'Error: No output produced'

        return f'STDOUT:\n{out}\n STDERR:\n{err}'
    except Exception as e: 
        return f"Error: executing Python file: {e}"
    
    
