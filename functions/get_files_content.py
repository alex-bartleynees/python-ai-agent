import os
from google.genai import types
from functions.is_subpath import is_subpath

MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    if not is_subpath(full_path, working_directory):
        return f"Error: Cannot read {file_path} as it is outside the permitted working directory"
    if not os.path.isfile(full_path):
        return f"Error: {file_path} does not exist"
    try:
        with open(full_path, "r") as file:
            content = file.read()
            if len(content) > MAX_CHARS:
                content = (
                    content[:MAX_CHARS]
                    + f"...File {file_path} truncated at {MAX_CHARS} characters"
                )
        return content
    except Exception as e:
        return f"Error: {str(e)}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a file in the specified directory, maximum file length is 10000 and constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to get the contents of, relative to the working directory. If a path to a file is not specified, produces an error.",
            ),
        },
    ),
)
