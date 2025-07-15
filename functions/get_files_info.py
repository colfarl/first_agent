import os

def get_files_info(working_directory, directory=None):
 
    full_path = os.path.join(working_directory, directory or "")
    abs_full  = os.path.abspath(full_path)
    abs_work  = os.path.abspath(working_directory)

    directory_name = "current" if directory == '.' else f"\'{directory}\'"
    elements_string = f"Result for {directory_name} directory:\n"

    if not abs_full.startswith(abs_work):
        return f'{elements_string} Error: Cannot list \"{directory}\" as it is outside the permitted working directory'
    
    if not os.path.isdir(full_path):
        return f'{elements_string} Error:\"{directory}\" is not a directory'
    
    for elem in os.listdir(abs_full):
        path = os.path.abspath(os.path.join(full_path, elem))

        is_dir = True
        if os.path.isfile(path):
            is_dir = False

        size = os.path.getsize(path)
        elements_string += f'- {elem}: file_size={size} bytes, is_dir={is_dir}\n'
     
    return elements_string
