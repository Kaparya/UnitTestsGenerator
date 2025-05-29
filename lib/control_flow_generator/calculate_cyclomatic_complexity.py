import ast
from typing import Dict, Union


class ComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 0

    def increment(self):
        self.complexity += 1

    def visit_If(self, node):
        self.increment()
        self.generic_visit(node)

    def visit_For(self, node):
        self.increment()
        self.generic_visit(node)

    def visit_While(self, node):
        self.increment()
        self.generic_visit(node)

    def visit_Try(self, node):
        self.increment()
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_Assert(self, node):
        self.increment()
        self.generic_visit(node)

    def visit_With(self, node):
        self.increment()
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self.increment()
        self.generic_visit(node)

    def visit_comprehension(self, node):
        self.increment()
        self.generic_visit(node)


def calculate_function_complexity(node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> int:
    visitor = ComplexityVisitor()
    visitor.visit(node)
    return visitor.complexity + 1


def analyze_file_complexity(filepath: str) -> Dict[str, int]:
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()

    tree = ast.parse(code)
    complexities = {}

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            complexity = calculate_function_complexity(node)
            complexities[node.name] = complexity

    return complexities
