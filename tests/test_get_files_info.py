import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from functions.get_files_info import get_files_info, FileInfo


def main() -> None:
    working_dir: str = "calculator"

    root_contents = get_files_info(working_dir, ".")
    if isinstance(root_contents, list):
        for f in root_contents:
            print(f"- {f.name}: file_size={f.file_size} bytes, is_dir={f.is_dir}")
    else:
        print(root_contents)
    print()

    pkg_contents = get_files_info(working_dir, "pkg")
    if isinstance(pkg_contents, list):
        for f in pkg_contents:
            print(f"- {f.name}: file_size={f.file_size} bytes, is_dir={f.is_dir}")
    else:
        print(pkg_contents)
    print()

    error_result = get_files_info(working_dir, "..")
    print(error_result)


main()
