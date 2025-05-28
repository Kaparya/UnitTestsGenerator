import ast


class ConditionExtractor(ast.NodeVisitor):
    def __init__(self):
        self.paths = []
        self.current_path = []

    def visit_If(self, node):
        self.current_path.append(ast.unparse(node.test))
        self.generic_visit(node)
        self.current_path.pop()

    def visit_For(self, node):
        self.current_path.append([ast.unparse(node.target), ast.unparse(node.iter)])
        self.generic_visit(node)
        self.current_path.pop()

    def visit_While(self, node):
        self.current_path.append(ast.unparse(node.test))
        self.generic_visit(node)
        self.current_path.pop()

    def visit_Return(self, node):
        path = list(self.current_path)  # сохраняем копию пути
        self.paths.append(path)
        # Не забудем обойти вложенные узлы внутри return (например, return f(x))
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
                function_ifs[node.name] = extractor.paths

        return function_ifs
