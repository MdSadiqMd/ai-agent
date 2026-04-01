import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dotenv import load_dotenv
from google import genai
from main import AgentConfig, agent_loop


def main() -> None:
    load_dotenv()
    api_key: str | None = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set")

    client: genai.Client = genai.Client(api_key=api_key)
    config: AgentConfig = AgentConfig(verbose=True)

    print("Test 1: list files")
    result: str | None = agent_loop(client, "what files are in the root?", config)
    if result is not None:
        print(f"Final response: {result}")
    else:
        print("No final response (max iterations reached)")
    print()

    print("Test 2: read a file")
    result = agent_loop(client, "read the contents of main.py", config)
    if result is not None:
        print(f"Final response: {result}")
    else:
        print("No final response (max iterations reached)")
    print()

    print("Test 3: run tests")
    result = agent_loop(client, "run tests.py", config)
    if result is not None:
        print(f"Final response: {result}")
    else:
        print("No final response (max iterations reached)")


main()
