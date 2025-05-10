import ast


def get_functions(file_path: str) -> list[str]:
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
