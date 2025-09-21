import os
from functions.is_subpath import is_subpath


def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    if not is_subpath(full_path, working_directory):
        return f"Error: Cannot read {file_path} as it is outside the permitted working directory"
    if not os.path.isfile(full_path):
        return f"Error: {file_path} does not exist"
    try:
        with open(full_path, "r") as file:
            content = file.read()
        return content
    except Exception as e:
        return f"Error: {str(e)}"
