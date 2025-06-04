from typing import List, Tuple, Union
from z3 import Int, And, Or, Not, Solver, sat


Interval = Tuple[Union[int, float], Union[int, float]]


def expand_expressions(expr_str: str, delimiter: str, orig_exprs: bool) -> list[str]:
    
    operands = {
        '==': '!=',
        '!=': '==',
        '>=': '<',
        '<=': '>',
        '>': '<=',
        '<': '>='
    }

    extended_expr = []
    for expr in expr_str.split(delimiter):
        if orig_exprs:
            extended_expr.append(expr)
        else:
            for oper, neg_oper in operands.items():
                if oper in expr:
                    extended_expr.append(expr.replace(oper, neg_oper))
                    break
    
    return extended_expr


def solve_conditions(exprs, var_names, number_of_solutions=3, var_range=(-1e9, 1e9), orig_exprs=True):
    for i in range(len(exprs)):
        exprs[i] = (
            exprs[i].replace("&", " and ").replace("|", " or ").replace("~", " not ")
        )
    expr_str = " and ".join(exprs)
    print("=========", expr_str)
    if expr_str[-4:-1] == "and":
        expr_str = expr_str[:-4]
    variables = {v: Int(v) for v in var_names}

    context = {**variables, "And": And, "Or": Or, "Not": Not}
    try:
        if " or " in expr_str:
            parts = [eval(part, context) for part in expand_expressions(expr_str, " or ", orig_exprs)]
            z3_expr = Or(*parts)
        elif " and " in expr_str:
            parts = [eval(part, context) for part in expand_expressions(expr_str, " and ", orig_exprs)]
            z3_expr = And(*parts)
        else:
            z3_expr = eval(expr_str, context)
    except Exception as e:
        print(f"Ошибка при парсинге выражения: {e}\nВыражение: {expr_str}")
        return None

    # Решаем
    s = Solver()
    s.add(z3_expr)
        
    for v in variables.values():
        s.add(v >= var_range[0], v <= var_range[1])

    results = []

    while len(results) < number_of_solutions and s.check() == sat:
        model = s.model()
        result = {str(d): model[d] for d in model}
        if result not in results:  # избегаем дубликатов
            results.append(result)

        # Запрещаем текущее решение
        s.add(Or(*[variables[k] != v for k, v in result.items()]))

    return results
