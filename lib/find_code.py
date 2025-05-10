import ast
import os


def find_all_code_files(folder_path: str) -> list[str]:
    """
    Find all code files in the given folder path.
    Args:
        folder_path (str): А path to the folder to search for code files.
    Returns:
        list[str]: A list of paths to the code files found in the folder.
    """
    code_files = []

    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if not d.startswith((".", "__"))]

        for file in files:
            if file.endswith(".py") and not file.startswith(("__init__", "test_")):
                code_files.append(os.path.join(root, file))

    return code_files


def get_functions_from_file(file_path: str) -> list[str]:
    """
    Find and return all functions in python file
    Args:
        file_path (str): The path to the file to generate tests for.
    Returns:
        list: list of strings where each string is the name of the function in file
    """
    with open(file_path, "r", encoding="utf-8") as f:
        file_content = f.read()

    tree = ast.parse(file_content, filename=file_path)
    functions = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]

    return functions
