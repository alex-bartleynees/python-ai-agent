import os
import subprocess

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
