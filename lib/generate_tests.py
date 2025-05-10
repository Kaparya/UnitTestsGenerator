import lib.parse_raw_file as parse_raw_file

from lib.save_file import save_file


def generate_tests(file_paths: list[str], canonize: bool = False) -> list[str]:
    """
    Generate test files for the given list of file paths.
    Args:
        file_paths (list[str]): A list of paths to the files to generate tests for.
        canonize (bool): Whether to canonize the generated tests (default: False).
    Returns:
        str: The generated test file (or files) location.
    """
    generated_pathes = []

    for file_path in file_paths:
        generated_tests = generate_test_file(file_path, canonize)
        generated_pathes.append(save_file(file_path, generated_tests))
    return generated_pathes


def generate_test_file(file_path: str, canonize: bool = False) -> str:
    """
    Returns:
        str: The generated test file content.
    """

    functions = parse_raw_file.get_functions(file_path)
    imports = parse_raw_file.get_imports(file_path)

    text_func = ""
    for lib in imports:
        text_func += f"{lib}\n"

    text_func += "\n\n"

    for function in functions:
        text_func += f"def test_{function}():\n"
        text_func += f"    assert 1 + 1 == 2\n\n"
    return text_func
