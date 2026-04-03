import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dotenv import load_dotenv
from google import genai
from main import Part, Content, AgentConfig, agent_loop


def main() -> None:
    # Test 1: Pydantic models
    part: Part = Part(text="hello")
    assert part.text == "hello"
    print(f"Part: {part.model_dump()}")

    content: Content = Content(role="user", parts=[Part(text="test")])
    assert content.role == "user"
    assert len(content.parts) == 1
    print(f"Content: {content.model_dump()}")

    config: AgentConfig = AgentConfig(verbose=True, max_iterations=5)
    assert config.model == "gemini-2.5-flash"
    assert config.max_iterations == 5
    assert config.verbose is True
    assert len(config.system_prompt) > 0
    print(
        f"AgentConfig model={config.model} max_iterations={config.max_iterations} verbose={config.verbose}"
    )
    print()

    # Test 2: Agent loop - list files
    load_dotenv()
    api_key: str | None = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        print("Skipping API tests: GEMINI_API_KEY not set")
        return

    client: genai.Client = genai.Client(api_key=api_key)

    print("Agent loop: list files")
    result: str | None = agent_loop(client, "what files are in the root?", config)
    if result is not None:
        print(f"Final: {result[:200]}")
    else:
        print("No final response")
    print()

    # Test 3: Agent loop - run tests
    print("Agent loop: run tests")
    result = agent_loop(client, "run tests.py and tell me if they pass", config)
    if result is not None:
        print(f"Final: {result[:200]}")
    else:
        print("No final response")


main()
