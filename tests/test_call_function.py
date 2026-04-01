import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from google.genai import types
from functions.call_function import call_function


def print_result(result: types.Content) -> None:
    if result.parts is not None and len(result.parts) > 0:
        response = result.parts[0].function_response
        if response and response.response:
            print(f"Result: {response.response}")


def main() -> None:
    fc = types.FunctionCall(name="get_files_info", args={"directory": "."})
    print_result(call_function(fc, verbose=True))
    print()

    fc = types.FunctionCall(name="get_file_content", args={"file_path": "main.py"})
    print_result(call_function(fc, verbose=True))
    print()

    fc = types.FunctionCall(name="run_python_file", args={"file_path": "tests.py"})
    print_result(call_function(fc, verbose=True))
    print()

    fc = types.FunctionCall(
        name="write_file",
        args={"file_path": "test_output.txt", "content": "hello from test"},
    )
    print_result(call_function(fc, verbose=True))
    print()

    fc = types.FunctionCall(name="nonexistent_func", args={})
    print_result(call_function(fc, verbose=True))
    print()

    fc = types.FunctionCall(name="get_files_info", args={"directory": "pkg"})
    print_result(call_function(fc))


main()
