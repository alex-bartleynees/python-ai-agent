import os

from functions.is_subpath import is_subpath


def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    if not is_subpath(full_path, working_directory):
        return f"Error: Cannot read {file_path} as it is outside the permitted working directory"

    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {str(e)}"

