import os
import subprocess
from pydantic import BaseModel
from google.genai import types


class PythonResult(BaseModel):
    stdout: str
    stderr: str
    return_code: int


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    abs_working_directory: str = os.path.abspath(working_directory)
    abs_file_path: str = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    try:
        command: list[str] = ["python", abs_file_path]
        if args:
            command.extend(args)

        result: subprocess.CompletedProcess[str] = subprocess.run(
            command,
            cwd=abs_working_directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        parsed: PythonResult = PythonResult(
            stdout=result.stdout,
            stderr=result.stderr,
            return_code=result.returncode,
        )

        output: str = ""
        if parsed.return_code != 0:
            output += f"Process exited with code {parsed.return_code}\n"

        if not parsed.stdout and not parsed.stderr:
            output += "No output produced"
        else:
            if parsed.stdout:
                output += f"STDOUT:\n{parsed.stdout}"
            if parsed.stderr:
                output += f"STDERR:\n{parsed.stderr}"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file: types.FunctionDeclaration = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional command-line arguments and returns the output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of command-line arguments to pass to the script",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
        required=["file_path"],
    ),
)
