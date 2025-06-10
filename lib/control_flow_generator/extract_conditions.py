import ast
import logging


logger = logging.getLogger(__name__)


class ConditionExtractor(ast.NodeVisitor):
    def __init__(self):
        self.paths = []
        self.current_path = []

    def visit_If(self, node):
        # cur_idx = len(self.current_path)
        self.current_path.append(ast.unparse(node.test))
        self.generic_visit(node)
        # self.current_path = self.current_path[:cur_idx]

    def visit_For(self, node):
        self.current_path.append(
            f"{ast.unparse(node.target)} in {ast.unparse(node.iter)}"
        )
        self.generic_visit(node)
        self.current_path.pop()

    def visit_While(self, node):
        self.current_path.append(ast.unparse(node.test))
        self.generic_visit(node)
        self.current_path.pop()

    def visit_Return(self, node):
        path = list(self.current_path)
        self.paths.append(path)
        self.generic_visit(node)


def extract_conditions(file_path: str):
    logger.debug(f"Extracting conditions from file")
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
        tree = ast.parse(source)

        function_ifs = {}
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                extractor = ConditionExtractor()
                extractor.visit(node)
                function_ifs[node.name] = extractor.paths

        return function_ifs
