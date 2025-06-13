from lib import find_all_code_files, generate_tests, print_metrics
from lib.save_file import create_conftest

import argparse
import logging
import os
import subprocess


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s || %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


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
        action="store_false",
    )
    parser.add_argument(
        "-pd",
        "--project_directory",
        help="Path to the project directory root",
    )
    parser.add_argument(
        "--cov",
        help="Code coverage analysis",
        action="store_true",
    )
    logging.info("UnitTestsGenerator started")

    args = parser.parse_args()
    if not (args.file_path or args.folder_path):
        parser.print_help()
        exit(1)

    if args.file_path:
        logging.info(f"Detected file path: {args.file_path}")
        if not args.project_directory:
            print("Project directory must be specified when using a file path.")
            exit(2)

        project_directory = args.project_directory
        create_conftest(project_directory)
        pytest_pathes, metrics = generate_tests(
            [args.file_path], project_directory, args.canonize
        )
    elif args.folder_path:
        code_files = find_all_code_files(args.folder_path)
        logging.info(
            f"Detected folder path: {args.folder_path} with {len(code_files)} code files"
        )

        project_directory = args.folder_path
        if args.project_directory:
            project_directory = args.project_directory

        create_conftest(project_directory)
        pytest_pathes, metrics = generate_tests(
            code_files, project_directory, args.canonize
        )

    logging.info(f"Tests generated, starting pytest")
    if args.cov and os.path.isdir(project_directory):
        pytest_pathes = pytest_pathes + [
            f"--cov={project_directory}",
            "--cov-report=term-missing",
            "--cov-config=.coveragerc",
        ]

    subprocess.run(["pytest", *pytest_pathes, "--disable-warnings"])

    print_metrics(metrics)


if __name__ == "__main__":
    main()
