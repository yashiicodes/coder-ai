from functions.get_file_content import get_file_content  # replace with actual module
from config import FILE_MAX_CHARS

def test_lorem_file():
    print("Testing lorem.txt (truncation check):")

    result = get_file_content("calculator", "lorem.txt")
    print(result)

def run_tests():
    # 1. Large file test
    test_lorem_file()

    # 2. Normal file
    print("\nResult for main.py:")
    print(get_file_content("calculator", "main.py"))

    # 3. Nested file
    print("\nResult for pkg/calculator.py:")
    print(get_file_content("calculator", "pkg/calculator.py"))

    # 4. Outside directory (should error)
    print("\nResult for '/bin/cat':")
    print(get_file_content("calculator", "/bin/cat"))

    # 5. Non-existent file (should error)
    print("\nResult for missing file:")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))


if __name__ == "__main__":
    run_tests()