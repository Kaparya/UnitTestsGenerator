from lib import generate_tests
from lib import find_all_code_files
from lib.save_file import create_conftest

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
        "-c",
        "--canonize",
        help="Canonize generated tests",
        action="store_true",
    )
    parser.add_argument(
        "-pd",
        "--project_directory",
        help="Path to the project directory root",
    )

    args = parser.parse_args()
    if not (args.file_path or args.folder_path):
        parser.print_help()
        exit(1)

    if args.file_path:
        if not args.project_directory:
            print("Project directory must be specified when using a file path.")
        create_conftest(args.project_directory)
        pytest_pathes = generate_tests(
            [args.file_path], args.project_directory, args.canonize
        )
    elif args.folder_path:
        code_files = find_all_code_files(args.folder_path)
        project_directory = args.folder_path
        if args.project_directory:
            project_directory = args.project_directory
        create_conftest(project_directory)
        pytest_pathes = generate_tests(code_files, project_directory, args.canonize)

    pytest.main(pytest_pathes)


if __name__ == "__main__":
    main()
