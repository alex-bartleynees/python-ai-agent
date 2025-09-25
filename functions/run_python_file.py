import os
import subprocess
from google.genai import types

from functions.is_subpath import is_subpath


def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    current_directory = os.getcwd()
    if not is_subpath(full_path, working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found'
    if not file_path.endswith(".py"):
        return f"Error: {file_path} is not a Python file."

    try:
        result = subprocess.run(
            ["python", full_path] + args,
            cwd=current_directory,
            timeout=30,
            capture_output=True,
            text=True,
            check=True,
        )
        if result.stdout:
            return f"STDOUT:\n{result.stdout}"
        if result.stderr:
            return f"STDERR:\n{result.stderr}"
        return "No output produced."
    except subprocess.TimeoutExpired:
        return "Error: Execution timed out."
    except subprocess.CalledProcessError as e:
        return f"Error: Process exited with code {str(e.returncode)}"
    except Exception as e:
        return f"Error: exceuting Python file: {str(e)}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified Python file within the working directory and returns its output or any errors encountered during execution.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to get the contents of, relative to the working directory. If a path to a file is not specified, produces an error.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of arguments to pass to the Python file when executing it.",
            ),
        },
    ),
)
