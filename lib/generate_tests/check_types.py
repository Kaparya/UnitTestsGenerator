from .generate_random_value import generate_random_value
from .check_values import (
    add_project_path,
    load_functions_dynamically,
    clear_project_path,
)
from lib.save_file import create_path_testfile
import lib.parse_raw_file as parse_raw_file


def add_types_tests(
    file_path: str, module_name: str, project_directory: str, canonize: bool
) -> str:
    """
    Generate test functions to test declared and actual outputs of functions.
    Returns:
        str: The generated text of tests.
    """

    test_file_path = create_path_testfile(file_path)
    functions_from_testfile = parse_raw_file.get_functions_info(test_file_path)
    add_project_path(project_directory)

    text_func = ""

    for name, function in load_functions_dynamically(file_path, module_name).items():
        if canonize and ("test_types_" + name) in functions_from_testfile.keys():
            text_func += functions_from_testfile["test_types_" + name]
            text_func += "\n\n"
            continue
        if function["returns"] is None or function["returns"] == "None":
            continue

        input = [generate_random_value(arg) for arg in function["args"]]

        exception_name = None
        try:
            result = function["exec"](*input)
        except Exception as e:
            exception_name = type(e).__name__

        if exception_name is None:
            input_text = ", ".join([str(arg) for arg in input])
            text_func += f"def test_types_{name}():\n"
            clean_return_type = function["returns"].split("[")[0].split("(")[0]

            if " " in clean_return_type:
                clean_return_type = "None.__class__"

            text_func += (
                f"    assert type({name}({input_text})) == {clean_return_type}\n\n"
            )
    clear_project_path()

    return text_func
