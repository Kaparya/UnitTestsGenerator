import ast


class ConditionExtractor(ast.NodeVisitor):
    def __init__(self):
        self.conditions = []

    def visit_If(self, node):
        self.conditions.append(ast.unparse(node.test))
        self.generic_visit(node)


def extract_conditions(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
        tree = ast.parse(source)

        function_ifs = {}
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                print(f"Function name: {node.name}")
                extractor = ConditionExtractor()
                extractor.visit(node)
                function_ifs[node.name] = extractor.conditions

        return function_ifs
