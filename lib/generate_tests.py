from lib.save_file import save_file

import importlib.util
import os
import sys
import types


def generate_tests(file_paths: list[str]):
    """
    Generate test files for the given list of file paths.
    Args:
        file_paths (list[str]): A list of paths to the files to generate tests for.
    """
    for file_path in file_paths:
        generated_tests = generate_test_file(file_path)
        save_file(file_path, generated_tests)


def generate_test_file(file_path: str) -> str:
    """
    Generate a test file for the given file path.
    Args:
        file_path (str): The path to the file to generate tests for.
    Returns:
        str: The generated test file content.
    """
    # TODO: Write logic to generate test for funcs

    functions = get_functions_from_file(file_path)
    text_func = "import pytest\n\n"
    for function in functions:
        text_func += f"def test_{function}():\n"  
        text_func += "    assert 1 + 1 == 2\n\n"        
    return text_func

    
def get_functions_from_file(file_path: str) -> list:
    """
    Find and return all functions in python file
    Args:
        file_path (str): The path to the file to generate tests for.
    Returns:
        list: list of strings where each string is the name of the function in file
    """

    abs_path = os.path.abspath(file_path)
    module_name = os.path.splitext(os.path.basename(file_path))[0]

    spec = importlib.util.spec_from_file_location(module_name, abs_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    functions = [
        name for name, obj in vars(module).items()
        if callable(obj) and isinstance(obj, types.FunctionType)
    ]

    return functions