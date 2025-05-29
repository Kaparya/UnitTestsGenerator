import ast


class ConditionExtractor(ast.NodeVisitor):
    def __init__(self):
        self.paths = []
        self.current_path = []
        self.seen_paths = set()  
    
    def visit_If(self, node):
        self.current_path.append(("if", ast.unparse(node.test)))
        self.generic_visit(node)
        self.current_path.pop()

        if node.orelse:
            self.current_path.append(("else", ast.unparse(node.test)))
            self.generic_visit(node)
            self.current_path.pop()

    def visit_For(self, node):
        self.current_path.append(("for", f"{ast.unparse(node.target)} in {ast.unparse(node.iter)}"))
        self.generic_visit(node)
        self.current_path.pop()

    def visit_While(self, node):
        self.current_path.append(("while", ast.unparse(node.test)))
        self.generic_visit(node)
        self.current_path.pop()

    def visit_Return(self, node):
        path = tuple(self.current_path)  
        if path not in self.seen_paths:
            self.seen_paths.add(path)
            self.paths.append(list(path))  
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
