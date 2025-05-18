from .generate_random_value import generate_random_value
import lib.parse_raw_file as parse_raw_file
from .check_values import add_project_path, load_functions_dynamically, clear_project_path

def add_types_tests(file_path: str, module_name: str, project_directory: str, canonize: bool) -> str:
    """
    Generate test functions to test declared and actual outputs of functions.
    Returns:
        str: The generated text of tests.
    """

    add_project_path(project_directory)

    text_func = ""
    functions_info = parse_raw_file.get_functions_info(file_path)

    for name, function in load_functions_dynamically(file_path, module_name).items():
    
        if function["returns"] is None or function["returns"] == "None":
            continue

        input = [
            generate_random_value(arg) for arg in function["args"]
        ]

        exception_name = None
        try:
            result = function["exec"](*input)
        except Exception as e:
            exception_name = type(e).__name__

        if exception_name is None:
            input_text = ", ".join([str(arg) for arg in input])
            text_func += f"def test_types_{name}():\n"
            clean_return_type = function["returns"].split("[")[0].split("(")[0]
            text_func += f"    assert type({name}({input_text})) == {clean_return_type}\n\n"
        
    clear_project_path()

    return text_func