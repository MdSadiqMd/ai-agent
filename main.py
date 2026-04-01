import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.types import GenerateContentResponse
from pydantic import BaseModel
from functions.call_function import available_functions, call_function


class Part(BaseModel):
    text: str


class Content(BaseModel):
    role: str
    parts: list[Part]


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py <prompt>")
        sys.exit(2)

    verbose_flag: bool = len(sys.argv) >= 3 and sys.argv[2] == "--verbose"

    load_dotenv()
    api_key: str | None = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set")

    system_prompt: str = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan.
You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory.
You do not need to specify the working directory in your function calls
as it is automatically injected for security reasons.
"""

    prompt: str = sys.argv[1]
    client: genai.Client = genai.Client(api_key=api_key)
    messages: list[Content] = [Content(role="user", parts=[Part(text=prompt)])]

    response: GenerateContentResponse = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    if response.function_calls:
        function_results: list[types.Part] = []
        for fc in response.function_calls:
            function_call_result: types.Content = call_function(
                fc, verbose=verbose_flag
            )
            if not function_call_result.parts:
                raise RuntimeError("Function call returned no parts")

            function_response = function_call_result.parts[0].function_response
            if function_response is None:
                raise RuntimeError("Function call returned no function_response")
            if function_response.response is None:
                raise RuntimeError("Function call returned no response")

            function_results.append(function_call_result.parts[0])
            if verbose_flag:
                print(f"-> {function_response.response}")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
