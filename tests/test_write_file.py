from functions.write_file import write_file, WriteResult


def main() -> None:
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    if isinstance(result, WriteResult):
        print(
            f'Successfully wrote to "{result.file_path}" ({result.chars_written} characters written)'
        )
    else:
        print(result)
    print()

    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    if isinstance(result, WriteResult):
        print(
            f'Successfully wrote to "{result.file_path}" ({result.chars_written} characters written)'
        )
    else:
        print(result)
    print()

    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    if isinstance(result, WriteResult):
        print(
            f'Successfully wrote to "{result.file_path}" ({result.chars_written} characters written)'
        )
    else:
        print(result)


main()
