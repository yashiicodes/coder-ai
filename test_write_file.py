from functions.write_file import write_file  # replace with actual module


def run_tests():
    # 1. Overwrite existing file
    print("Test 1: Overwrite lorem.txt")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

    # 2. Create new file in subdirectory
    print("\nTest 2: Write to pkg/morelorem.txt")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

    # 3. Outside directory (should fail)
    print("\nTest 3: Write to /tmp/temp.txt")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))


if __name__ == "__main__":
    run_tests()