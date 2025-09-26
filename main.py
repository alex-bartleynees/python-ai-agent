import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_files_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    args = sys.argv[1:]

    if not args:
        print("Please provide a prompt as a command line argument.")
        sys.exit(1)

    verbose_mode = ""
    if "--verbose" in args:
        verbose_mode = "--verbose"
        args = [arg for arg in args if arg != "--verbose"]

    user_prompt = " ".join(args)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    client = genai.Client(api_key=api_key)

    while len(messages) < 20:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt, tools=[available_functions]
                ),
            )

            for candidate in response.candidates:
                messages.append(candidate.content)

            if verbose_mode:
                print("User prompt:", user_prompt)
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print(
                    "Response tokens:", response.usage_metadata.candidates_token_count
                )

            if response.function_calls:
                for function_call in response.function_calls:
                    function_response = call_function(
                        function_call, verbose=bool(verbose_mode)
                    )
                    response_content = function_response.parts[
                        0
                    ].function_response.response
                    if response_content:
                        messages.append(
                            types.Content(
                                role="user",
                                parts=[types.Part(text=str(response_content))],
                            )
                        )
                        if verbose_mode:
                            print(f"-> {response_content}")
                    else:
                        raise ValueError("Function response is missing or malformed.")
            elif response.text:
                print(response.text)
                break
        except Exception as e:
            print(f"Error occurred: {e}")
            break


if __name__ == "__main__":
    main()
