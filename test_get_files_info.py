from functions.get_files_info import get_files_info  # replace with actual file name


def run_tests():
    # Test 1: current directory
    print("Result for current directory:")
    result = get_files_info("calculator", ".")
    print(format_output(result))

    # Test 2: pkg directory
    print("\nResult for 'pkg' directory:")
    result = get_files_info("calculator", "pkg")
    print(format_output(result))

    # Test 3: restricted directory (/bin)
    print("\nResult for '/bin' directory:")
    result = get_files_info("calculator", "/bin")
    print(format_output(result))

    # Test 4: parent directory (../)
    print("\nResult for '../' directory:")
    result = get_files_info("calculator", "../")
    print(format_output(result))


def format_output(result):
    # If error → indent differently
    if result.startswith("Error:"):
        return f"    {result}"
    
    # Otherwise indent each line
    lines = result.split("\n")
    return "\n".join([f"  {line}" for line in lines])


if __name__ == "__main__":
    run_tests()