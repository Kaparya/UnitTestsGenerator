import re
import random
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

    module_name  = re.split(r"[\\/]+", file_path)[-1].split(".")[0]
    functions = parse_raw_file.get_functions(file_path)
    imports = parse_raw_file.get_imports(file_path)

    text_func = ""
    for lib in imports:
        text_func += f"{lib}\n"
    text_func += f"from {module_name} import " + ", ".join(functions)
    text_func += "\n\n"

    for function in functions:
        text_func += f"def test_{function}():\n"
        text_func += f"    assert 1 + 1 == 2\n\n"

    additional_tests = add_input_output_tests(file_path)
    text_func += additional_tests
    
    return text_func

def add_input_output_tests(file_path: str) -> str:
    """
    Generate test functions to test declared and actual outputs of functions.
    Args:
        file_paths (str): A pathmto the file to generate tests for.
    Returns:
        str: The generated text of tests.
    """
    text_func = ''
    functions_info = parse_raw_file.get_functions_info(file_path)
    for func in functions_info:
        print(1)
        text_func += f"def test_{func['name']}():\n"
        input = [str(generate_random_value(annotation)) for annotation in func['inputs']]
        print(func['name'])
        input_text = ", ".join(input)
        text_func += f"    assert type({func['name']}({input_text})) == {func['return_type']}\n\n"

    return text_func

def generate_random_value(annotation):
    if annotation == "int":
        return random.randint(0, 100)
    elif annotation == "float":
        return round(random.uniform(0.0, 100.0), 2)
    elif annotation == "str":
        return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=5))
    elif annotation == "bool":
        return random.choice([True, False])
    elif annotation.startswith("list") or annotation.startswith("List"):
        return [random.randint(0, 10) for _ in range(3)]
    elif annotation.startswith("dict") or annotation.startswith("Dict"):
        return {str(i): random.randint(0, 10) for i in range(3)}
    elif annotation.startswith("Optional"):
        return random.choice([generate_random_value(annotation[9:-1]), None])
    return None

    

    