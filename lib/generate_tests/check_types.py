from .generate_random_value import generate_random_value

import lib.parse_raw_file as parse_raw_file


def add_types_tests(file_path: str) -> str:
    """
    Generate test functions to test declared and actual outputs of functions.
    Args:
        file_paths (str): A path to the file to generate tests for.
    Returns:
        str: The generated text of tests.
    """
    text_func = ""
    functions_info = parse_raw_file.get_functions_info(file_path)
    for func in functions_info:
        print(1)
        text_func += f"def test_types_{func['name']}():\n"
        input = [
            str(generate_random_value(annotation)) for annotation in func["inputs"]
        ]
        print(func["name"])
        input_text = ", ".join(input)
        clean_return_type = func["return_type"].split("[")[0].split("(")[0]
        text_func += (
            f"    assert type({func['name']}({input_text})) == {clean_return_type}\n\n"
        )

    return text_func
