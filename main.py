import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.types import GenerateContentResponse
from pydantic import BaseModel
from functions.call_function import available_functions, call_function

MAX_ITERATIONS: int = 20


class Part(BaseModel):
    text: str


class Content(BaseModel):
    role: str
    parts: list[Part]


class AgentConfig(BaseModel):
    model: str = "gemini-2.5-flash"
    max_iterations: int = MAX_ITERATIONS
    verbose: bool = False
    system_prompt: str = """
You are a helpful AI coding agent. You solve problems by exploring the codebase,
understanding the code, making changes, and verifying your fixes.

You can perform the following operations:
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

When solving a bug or completing a task, follow this workflow:
1. Explore: List files and read relevant code to understand the project structure.
2. Analyze: Identify the root cause of the issue.
3. Fix: Write the corrected code to the appropriate file.
4. Verify: Run the program or tests to confirm the fix works.

Important rules:
- All paths you provide should be relative to the working directory.
- You do not need to specify the working directory in your function calls
  as it is automatically injected for security reasons.
- When writing files, always write the COMPLETE file content, not just the changed parts.
- Always verify your changes by running the code after making edits.
"""


def agent_loop(client: genai.Client, prompt: str, config: AgentConfig) -> str | None:
    messages: list[types.Content | Content] = [
        Content(role="user", parts=[Part(text=prompt)])
    ]

    for _ in range(config.max_iterations):
        response: GenerateContentResponse = client.models.generate_content(
            model=config.model,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=config.system_prompt,
            ),
        )
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)
        if not response.function_calls:
            return response.text

        function_responses: list[types.Part] = []
        for fc in response.function_calls:
            function_call_result: types.Content = call_function(
                fc, verbose=config.verbose
            )
            if not function_call_result.parts:
                raise RuntimeError("Function call returned no parts")

            function_response = function_call_result.parts[0].function_response
            if function_response is None:
                raise RuntimeError("Function call returned no function_response")
            if function_response.response is None:
                raise RuntimeError("Function call returned no response")

            function_responses.append(function_call_result.parts[0])

            if config.verbose:
                print(f"-> {function_response.response}")

        messages.append(types.Content(role="user", parts=function_responses))

    return None


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py <prompt>")
        sys.exit(2)

    verbose_flag: bool = len(sys.argv) >= 3 and sys.argv[2] == "--verbose"

    load_dotenv()
    api_key: str | None = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set")

    config: AgentConfig = AgentConfig(verbose=verbose_flag)
    prompt: str = sys.argv[1]
    client: genai.Client = genai.Client(api_key=api_key)

    result: str | None = agent_loop(client, prompt, config)

    if result is not None:
        print(result)
    else:
        print("Max iterations reached. The agent could not complete the task.")
        sys.exit(1)


if __name__ == "__main__":
    main()
