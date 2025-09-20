import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    args = sys.argv[1:]

    if not args:
        print("Please provide a prompt as a command line argument.")
        sys.exit(1)

    user_prompt = " ".join(args[0])

    verbose_mode = ""
    if len(args) > 1:
        verbose_mode = args[1]

        if verbose_mode != "--verbose":
            print("Invalid second argument. Use --verbose for verbose mode.")
            sys.exit(1)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    if verbose_mode:
        print("User prompt:", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    print(response.text)


if __name__ == "__main__":
    main()
