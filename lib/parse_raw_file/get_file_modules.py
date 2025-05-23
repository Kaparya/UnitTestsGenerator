import ast
import os


def get_functions(file_path: str) -> list[str]:
    """
    Find and return all functions in python file
    Args:
        file_path (str): The path to the file to generate tests for.
    Returns:
        list: list of strings where each string is the name of the function in file
    """
    with open(file_path, "r") as f:
        file_content = f.read()

    tree = ast.parse(file_content, filename=file_path)
    functions = [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]

    return functions


def get_imports(file_path: str) -> list[str]:
    """
    Find and return all imports in python file
    Args:
        file_path (str): The path to the file to generate tests for.
    Returns:
        list: list of strings where each string is the name of the import in file
    """
    imports = []

    with open(file_path, "r") as f:
        for line in f:
            if line.startswith("import") or line.startswith("from"):
                imports.append(line.strip())

    return imports


def get_functions_info(file_path: str) -> dict:
    """
    Find and return all functions in file
    Args:
        file_path (str): The path to the file to generate tests for.
    Returns:
        dict: where key is function name, value is a text of function
    """

    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)
    functions = {}
    lines = source.splitlines()

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start_line = node.lineno - 1
            end_line = (
                node.end_lineno if hasattr(node, "end_lineno") else node.body[-1].lineno
            )
            func_text = "\n".join(lines[start_line:end_line])
            functions[node.name] = func_text

    return functions


def get_module_name(file_path: str, project_directory: str) -> str:
    if (
        not project_directory.startswith("./")
        and not project_directory == "."
        and project_directory in file_path
    ):
        file_path = file_path.replace(project_directory, "")

    module_name = file_path.split(".")[-2].replace("/", ".").replace("\\", ".")
    if module_name.startswith((".", "\\", "/")):
        module_name = module_name[1:]
    print("--------------", module_name, file_path)
    return module_name
