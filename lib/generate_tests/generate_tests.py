from .check_types import add_input_output_tests

import lib.parse_raw_file as parse_raw_file
from lib.save_file import save_file


def generate_tests(
    file_paths: list[str], project_directory: str, canonize: bool = False
) -> list[str]:
    """
    Generate test files for the given list of file paths.
    Args:
        file_paths (list[str]): A list of paths to the files to generate tests for.
        project_directory (str): The path to the project directory root.
        canonize (bool): Whether to canonize the generated tests (default: False).
    Returns:
        str: The generated test file (or files) location.
    """
    generated_pathes = []

    for file_path in file_paths:
        generated_tests = generate_test_file(file_path, project_directory, canonize)
        generated_pathes.append(save_file(file_path, generated_tests))
    return generated_pathes


def generate_test_file(
    file_path: str, project_directory: str, canonize: bool = False
) -> str:
    """
    Returns:
        str: The generated test file content.
    """

    module_name = parse_raw_file.get_module_name(file_path, project_directory)
    print("Current module name:", module_name)

    functions = parse_raw_file.get_functions(file_path)

    text_func = ""
    text_func += f"from {module_name} import " + ", ".join(functions)
    text_func += "\n\n"

    for function in functions:
        text_func += f"def test_{function}():\n"
        text_func += f"    assert 1 + 1 == 2\n\n"

    additional_tests = add_input_output_tests(file_path)
    text_func += additional_tests

    return text_func
