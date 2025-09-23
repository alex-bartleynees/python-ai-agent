import os
from google.genai import types
from functions.is_subpath import is_subpath


def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)

    if not is_subpath(full_path, working_directory):
        return f"Error: Cannot list {directory} as it is outside the permitted working directory"

    if not os.path.isdir(full_path):
        return f"Error: {directory} is not a directory"

    directory_contents = ""

    try:
        for item in os.listdir(full_path):
            item_path = os.path.join(full_path, item)
            item_info_string = f"{item}: file_size: {os.path.getsize(item_path)}, is_dir={os.path.isdir(item_path)}"
            directory_contents += item_info_string + "\n"
    except Exception as e:
        return f"Error: {str(e)}"

    return directory_contents.strip()


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
