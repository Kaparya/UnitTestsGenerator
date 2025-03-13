import ast
import itertools
import re


def extract_conditions(node):
    conditions = []
    if isinstance(node, ast.If):
        conditions.append(ast.unparse(node.test))
    elif isinstance(node, (ast.While, ast.For)):
        if isinstance(node, ast.While):
            conditions.append(ast.unparse(node.test))
        elif isinstance(node, ast.For):
            iter_range = node.iter
            if isinstance(iter_range, ast.Call) and iter_range.func.id == "range":
                args = [ast.unparse(arg) for arg in iter_range.args]
                conditions.append(f"range({', '.join(args)})")
    
    return conditions

def generate_tests(source_code):

    tree = ast.parse(source_code)
    conditions = []
    
    for node in ast.walk(tree):
        conditions.extend(extract_conditions(node))
    
    test_cases = []
    for cond in conditions:
        if "range" in cond:
            parts = cond.replace("range", "").strip("()").split(",")
            if len(parts) == 1:
                start, stop, step = 0, int(parts[0]), 1
            elif len(parts) == 2:
                start, stop, step = int(parts[0]), int(parts[1]), 1
            else:
                start, stop, step = map(int, parts)
            
            test_cases.append(f"Тест для диапазона: {start}, {stop}, {step}")
            test_cases.append(f"Граничные значения: {start}, {stop - step}")
        else:
            parts = re.split(r"[< > >= <= == ]", cond)
            bounds = [int(s) for s in parts if bool(re.fullmatch(r"-?\d+(\.\d+)?", s))]
            test_cases.append(f"Тест для условия: {cond}")
            test_cases.append(f"Граничные значения: {', '.join(map(str, bounds))}")

    return test_cases
