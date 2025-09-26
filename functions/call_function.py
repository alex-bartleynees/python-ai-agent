import os
import importlib
from google.genai import types


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    arguments = function_call_part.args
    if verbose:
        print(f"Calling function: {function_name}({arguments})")
    else:
        print(f" - Calling function: {function_name}")

    function_mapping = {
        "get_file_content": "functions.get_files_content.get_file_content",
        "get_files_info": "functions.get_files_info.get_files_info",
        "run_python_file": "functions.run_python_file.run_python_file",
        "write_file": "functions.write_file.write_file",
    }

    if function_name not in function_mapping:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    module_path, func_name = function_mapping[function_name].rsplit(".", 1)
    function_to_call = import_function(module_path, func_name)
    working_directory = os.getcwd()
    arguments["working_directory"] = working_directory
    function_result = function_to_call(**arguments)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


def import_function(module_path, function_name):
    module = importlib.import_module(module_path)
    return getattr(module, function_name)
