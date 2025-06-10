from .check_types import add_types_tests
from .check_values import add_values_tests

import lib.parse_raw_file as parse_raw_file
from lib.control_flow_generator import analyze_file_complexity, extract_conditions
from lib.save_file import save_file
import logging

logger = logging.getLogger(__name__)


def generate_tests(
    file_paths: list[str], project_directory: str, canonize: bool = False
) -> tuple[list[str], str]:
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
    result_str = ""

    for file_path in file_paths:
        generated_tests, total_complexity, total_tests = generate_test_file(
            file_path, project_directory, canonize
        )
        if total_tests > 0:
            generated_pathes.append(save_file(file_path, generated_tests))
            path = generated_pathes[-1]

            result_str += f"File {path.replace('tests/test_', '')} - complexity {total_complexity} | {total_tests} tests\n"
    return generated_pathes, result_str


def generate_test_file(
    file_path: str, project_directory: str, canonize: bool = False
) -> tuple[str, int, int]:
    """
    Returns:
        str: The generated test file content.
    """
    if not file_path.endswith(".py"):
        logger.debug(f"File {file_path} is not a Python file. Skipping.")
        return "", 0, 0

    logger.info(f"=== Generating tests for file: {file_path} === ")
    total_complexity = 0

    module_name = parse_raw_file.get_module_name(file_path, project_directory)
    functions = parse_raw_file.get_functions(file_path)

    text_func = "import pytest\n"
    text_func += f"from {module_name} import " + ", ".join(functions)
    text_func += "\n\n"

    complexities = analyze_file_complexity(file_path)
    conditions = extract_conditions(file_path)
    for name, complexity in complexities.items():
        total_complexity += complexity
        text_func += f"# Complexity of function {name} is {complexity}\n"
        for condition in conditions[name]:
            text_func += f"#    {condition}\n"
    text_func += "\n\n"

    values_tests, number_of_values_tests = add_values_tests(
        file_path, module_name, project_directory, conditions
    )
    types_tests, number_of_types_tests = add_types_tests(
        file_path, module_name, project_directory, canonize
    )
    text_func += types_tests
    text_func += values_tests

    return text_func, total_complexity, number_of_values_tests + number_of_types_tests
