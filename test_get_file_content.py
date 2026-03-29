from functions.get_file_content import get_file_content, FileContent


def main() -> None:
    result = get_file_content("calculator", "lorem.txt")
    if isinstance(result, FileContent):
        expected_truncation: str = '[...File "lorem.txt" truncated at 10000 characters]'
        print(f"Lorem length: {result.char_count}")
        print(f"Truncated: {result.content.endswith(expected_truncation)}")
    print()

    result = get_file_content("calculator", "main.py")
    if isinstance(result, FileContent):
        print(result.content)
    print()

    result = get_file_content("calculator", "pkg/calculator.py")
    if isinstance(result, FileContent):
        print(result.content)
    print()

    print(get_file_content("calculator", "/bin/cat"))
    print()

    print(get_file_content("calculator", "pkg/does_not_exist.py"))


main()
