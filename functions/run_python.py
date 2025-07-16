import os
import subprocess

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
    
    
