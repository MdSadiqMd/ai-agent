import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.types import GenerateContentResponse
from pydantic import BaseModel
from functions.call_function import available_functions


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
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        if verbose_flag:
            print(f"User prompt: {prompt}")
            if response.usage_metadata is not None:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(
                    f"Response tokens: {response.usage_metadata.candidates_token_count}"
                )
        print(response.text)


if __name__ == "__main__":
    main()
