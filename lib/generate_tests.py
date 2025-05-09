from lib.save_file import save_file

import ast
import importlib.util
import os
import sys
import types


def generate_tests(file_paths: list[str]) -> list[str]:
    """
    Generate test files for the given list of file paths.
    Args:
        file_paths (list[str]): A list of paths to the files to generate tests for.
    Returns:
        str: The generated test file (or files) location.
    """
    generated_pathes = []

    for file_path in file_paths:
        generated_tests = generate_test_file(file_path)
        generated_pathes.append(save_file(file_path, generated_tests))
    return generated_pathes


def generate_test_file(file_path: str) -> str:
    """
    Generate a test file for the given file path.
    Args:
        file_path (str): The path to the file to generate tests for.
    Returns:
        str: The generated test file content.
    """

    functions = get_functions_from_file(file_path)
    text_func = "import pytest\n\n"
    for function in functions:
        text_func += f"def test_{function}():\n"
        text_func += "    assert 1 + 1 == 2\n\n"
    return text_func


def get_functions_from_file(file_path: str) -> list[str]:
    """
    Find and return all functions in python file
    Args:
        file_path (str): The path to the file to generate tests for.
    Returns:
        list: list of strings where each string is the name of the function in file
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        file_content = f.read()

    tree = ast.parse(file_content, filename=file_path)

    functions = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]

    return functions
