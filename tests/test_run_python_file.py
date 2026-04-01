import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from functions.run_python_file import run_python_file


def main() -> None:
    print(run_python_file("calculator", "main.py"))
    print()

    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print()

    print(run_python_file("calculator", "tests.py"))
    print()

    print(run_python_file("calculator", "../main.py"))
    print()

    print(run_python_file("calculator", "nonexistent.py"))
    print()

    print(run_python_file("calculator", "lorem.txt"))


main()
