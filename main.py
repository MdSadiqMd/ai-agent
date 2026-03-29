import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentResponse
from google.genai import types
from pydantic import BaseModel


class Response(BaseModel):
    answer: str
    confidence: float


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py <prompt>")
        sys.exit(2)

    load_dotenv()
    api_key: str | None = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set")

    prompt: str = sys.argv[1]
    client: genai.Client = genai.Client(api_key=api_key)

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    response: GenerateContentResponse = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config={
            "response_mime_type": "application/json",
            "response_schema": Response,
        },
    )

    parsed: Response = Response.model_validate_json(response.text)
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Answer: {parsed.answer}")
    print(f"Confidence: {parsed.confidence}")


if __name__ == "__main__":
    main()
