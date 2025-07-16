import os

def write_file(working_directory, file_path, content):
    
    full_path = os.path.join(working_directory, file_path or "")
    abs_full  = os.path.abspath(full_path)
    abs_work  = os.path.abspath(working_directory)

    if not abs_full.startswith(abs_work):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_full) and os.path.exists(abs_full):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(abs_full, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except IOError as e:
        return f"Error: writing to file: {e}"
