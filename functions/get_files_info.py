import os
from pydantic import BaseModel


class FileInfo(BaseModel):
    name: str
    file_size: int
    is_dir: bool


def get_files_info(
    working_directory: str, directory: str = "."
) -> list[FileInfo] | str:
    abs_working_directory: str = os.path.abspath(working_directory)
    abs_directory: str = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_directory.startswith(abs_working_directory):
        return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"

    result: list[FileInfo] = []
    contents: list[str] = os.listdir(abs_directory)
    for content in contents:
        content_path: str = os.path.join(abs_directory, content)
        result.append(
            FileInfo(
                name=content,
                file_size=os.path.getsize(content_path),
                is_dir=os.path.isdir(content_path),
            )
        )
    return result
