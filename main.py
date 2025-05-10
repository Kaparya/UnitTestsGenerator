from lib import generate_tests
from lib import find_all_code_files

import argparse
import pytest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file_path",
        help="The path to the file to generate tests for",
    )
    parser.add_argument(
        "--folder_path",
        help="The path to the folder to generate tests for",
    )
    parser.add_argument(
        "-c", "--canonize",
        help="Canonize generated tests",
        action="store_true",
    )

    args = parser.parse_args()
    if not (args.file_path or args.folder_path):
        parser.print_help()
        exit(1)

    if args.file_path:
        pytest_pathes = generate_tests([args.file_path], args.canonize)
    elif args.folder_path:
        code_files = find_all_code_files(args.folder_path)
        pytest_pathes = generate_tests(code_files, args.canonize)

    pytest.main(pytest_pathes)


if __name__ == "__main__":
    main()
