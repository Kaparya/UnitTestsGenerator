from .generate_random_value import generate_random_value
from .check_values import (
    add_project_path,
    load_functions_dynamically,
    clear_project_path,
)
from lib.save_file import create_path_testfile
import lib.parse_raw_file as parse_raw_file

import logging

logger = logging.getLogger(__name__)


def add_types_tests(
    file_path: str, module_name: str, project_directory: str, canonize: bool
) -> str:
    """
    Generate test functions to test declared and actual outputs of functions.
    Returns:
        str: The generated text of tests.
    """
    number_of_tests = 0

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

        input = [generate_random_value(arg) for arg in function["args_types"]]

        exception_name = None
        previous_level = logger.level
        logger.setLevel(logging.CRITICAL + 1)
        try:
            result = function["exec"](*input)
        except Exception as e:
            exception_name = type(e).__name__
        finally:
            logger.setLevel(previous_level)

        if exception_name is None:
            number_of_tests += 1

            input_text = ", ".join([str(arg) for arg in input])
            text_func += f"def test_types_{name}():\n"
            clean_return_type = function["returns"].split("[")[0].split("(")[0]

            text_func += (
                f"    assert type({name}({input_text})) == {clean_return_type}\n\n"
            )
    clear_project_path()
    logger.info(f"Generated {number_of_tests} tests for types")
    return text_func
