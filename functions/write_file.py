import os
from google.genai import types
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


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file within the working directory, creating any necessary directories.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "write_file": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write the contents to, relative to the working directory. If a path to a file is not specified, produces an error.",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write the contents to, relative to the working directory. If a path to a file is not specified, produces an error.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the specified file.",
            ),
        },
    ),
)
