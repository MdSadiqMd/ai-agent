import os
from pydantic import BaseModel
from google.genai import types

MAX_CHARS: int = 10000


class FileContent(BaseModel):
    content: str
    file_path: str
    truncated: bool
    char_count: int


def get_file_content(working_directory: str, file_path: str) -> FileContent | str:
    abs_working_directory: str = os.path.abspath(working_directory)
    abs_file_path: str = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_file_path, "r") as f:
            file_content_string: str = f.read(MAX_CHARS)
            truncated: bool = len(file_content_string) >= MAX_CHARS
            if truncated:
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return FileContent(
            content=file_content_string,
            file_path=file_path,
            truncated=truncated,
            char_count=len(file_content_string),
        )
    except Exception as e:
        return f"Exception reading file: {e}"


schema_get_file_content: types.FunctionDeclaration = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)
