import os
from pydantic import BaseModel


class WriteResult(BaseModel):
    file_path: str
    chars_written: int


def write_file(
    working_directory: str, file_path: str, content: str
) -> WriteResult | str:
    abs_working_directory: str = os.path.abspath(working_directory)
    abs_file_path: str = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    parent_dir: str = os.path.dirname(abs_file_path)
    try:
        os.makedirs(parent_dir, exist_ok=True)
    except Exception as e:
        return f"Could not create parent dirs: {parent_dir} = {e}"

    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
        return WriteResult(
            file_path=file_path,
            chars_written=len(content),
        )
    except Exception as e:
        return f"Failed to write to file: {file_path} - {e}"
