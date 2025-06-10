from .generate_random_value import generate_random_value
from lib.control_flow_generator import solve_conditions, solve_string_conditions

import ast
import importlib.util
import logging
import os
import sys

logger = logging.getLogger(__name__)


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
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
            args_types = []
            args_names = []
            for arg in node.args.args:
                if arg.annotation:
                    annotation = ast.unparse(arg.annotation)
                    args_types.append(annotation)
                else:
                    args_types.append(None)
                args_names.append(arg.arg)
            functions.append(
                {
                    "name": node.name,
                    "args_types": args_types,
                    "args_names": args_names,
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
                    "args_names": cur_func["args_names"],
                    "args_types": cur_func["args_types"],
                    "returns": cur_func["returns"],
                }
    return functions


def add_values_tests(
    file_path: str,
    module_name: str,
    project_directory: str,
    conditions: dict[str, list[str]],
) -> str:
    """
    Generate test functions to test correct and actual outputs of functions.
    Returns:
        str: The generated text of tests.
    """
    if (
        not file_path.endswith(".py")
        or not os.path.isfile(file_path)
        or not os.path.isdir(project_directory)
    ):
        logger.debug(
            f"Something wrong with file {file_path} or project directory {project_directory}. Skipping."
        )
        return ""
    number_of_tests = 0
    add_project_path(project_directory)

    text_func = ""
    for name, function in load_functions_dynamically(file_path, module_name).items():
        # print(f"Function name: {name}")
        args_types = function["args_types"]
        args_names = function["args_names"]
        # print(f"Function args_names: {args_names}")
        # print(f"Function args_types: {args_types}")
        # print(f"Function return type: {function['returns']}")
        # print(f"Function conditions: {conditions.get(name, [])}")
        # if function["returns"] is None or function["returns"] == "None":
        #     print(f"Function {name} has no return type annotation. Skipping...")
        #     continue

        conditions_solution = []
        for condition in conditions.get(name, []):
            # print("+++++++++++", condition)
            if "str" in args_types:
                conditions_solution.append(
                    solve_string_conditions(exprs=condition, var_names=args_names)
                )
            else:
                conditions_solution.append(
                    solve_conditions(
                        exprs=condition,
                        var_names=args_names,
                        var_types=args_types,
                        orig_exprs=True,
                    )
                )
                conditions_solution.append(
                    solve_conditions(
                        exprs=condition,
                        var_names=args_names,
                        var_types=args_types,
                        orig_exprs=False,
                    )
                )
        # print(f"Conditions solution: {conditions_solution}")
        number_of_tests += 1
        text_func += f"def test_{name}_values():\n"
        for cur_test in range(3):
            args = []
            for arg_type in args_types:
                args.append(generate_random_value(arg_type))

            exception_name = None
            previous_level = logger.level
            logger.setLevel(logging.CRITICAL + 1)
            try:
                result = function["exec"](*args)
                if isinstance(result, str):
                    result = '"' + result + '"'
            except Exception as e:
                exception_name = type(e).__name__
                logger.debug(exception_name)
            finally:
                logger.setLevel(previous_level)

            if exception_name is None:
                text_func += (
                    f"    assert {name}({', '.join(map(str, args))}) == {result}\n"
                )
            else:
                text_func += f"    with pytest.raises({exception_name}):\n"
                text_func += f"        {name}({', '.join(map(str, args))})\n"
        text_func += "\n\n"
    clear_project_path()
    logger.info(f"Generated {number_of_tests} tests for values")
    return text_func
