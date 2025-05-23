from .generate_random_value import generate_random_value

import os
import sys
import ast
import importlib.util


def add_project_path(path):
    abs_path = os.path.abspath(path)
    if abs_path not in sys.path:
        sys.path.insert(0, abs_path)


def clear_project_path():
    sys.path.pop(0)


def parse_function_names(filepath: str):
    with open(filepath, "r") as f:
        source = f.read()

    tree = ast.parse(source, filename=filepath)
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args_types = []
            for arg in node.args.args:
                if arg.annotation:
                    annotation = ast.unparse(arg.annotation)
                    args_types.append(annotation)
                else:
                    args_types.append(None)
            functions.append(
                {
                    "name": node.name,
                    "args": args_types,
                    "defaults": node.args.defaults,
                    "returns": ast.unparse(node.returns) if node.returns else None,
                }
            )
    return functions


def import_module_from_file(filepath: str, module_name: str = "target_module"):
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {filepath}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_functions_dynamically(filepath: str, module_name: str):
    function_names = parse_function_names(filepath)
    module = import_module_from_file(filepath, module_name)

    functions = {}
    for cur_func in function_names:
        if hasattr(module, cur_func["name"]):
            func = getattr(module, cur_func["name"])
            if callable(func):
                functions[cur_func["name"]] = {
                    "exec": func,
                    "args": cur_func["args"],
                    "returns": cur_func["returns"],
                }

    return functions


def add_values_tests(file_path: str, module_name: str, project_directory: str) -> str:
    """
    Generate test functions to test correct and actual outputs of functions.
    Returns:
        str: The generated text of tests.
    """

    add_project_path(project_directory)

    text_func = ""
    for name, function in load_functions_dynamically(file_path, module_name).items():
        print(f"Function name: {name}")
        args_types = function["args"]
        print(f"Function args: {args_types}")
        print(f"Function return type: {function['returns']}")
        if function["returns"] is None or function["returns"] == "None":
            print(f"Function {name} has no return type annotation. Skipping...")
            continue

        text_func += f"def test_{name}_values():\n"
        for cur_test in range(3):
            args = []
            for arg_type in args_types:
                args.append(generate_random_value(arg_type))

            exception_name = None
            try:
                result = function["exec"](*args)
                if isinstance(result, str):
                    result = '"' + result + '"'
            except Exception as e:
                exception_name = type(e).__name__
                print(exception_name)

            if exception_name is None:
                text_func += (
                    f"    assert {name}({', '.join(map(str, args))}) == {result}\n"
                )
            else:
                text_func += f"    with pytest.raises({exception_name}):\n"
                text_func += f"        {name}({', '.join(map(str, args))})\n"
        text_func += "\n\n"
    clear_project_path()
    return text_func
