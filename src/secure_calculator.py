import ast
import operator
import datetime

class SecureCalculator:
    OPS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.FloorDiv: operator.floordiv,
        ast.USub: operator.neg
    }

    def __init__(self, log_file="calc_log.txt"):
        self.log_file = log_file

    def _log(self, message: str):
        timestamp = datetime.datetime.now().isoformat()
        safe = message.replace("\n", "\\n")
        with open(self.log_file, "a") as f:
            f.write(f"{timestamp} - {safe}\n")

    def evaluate(self, expression: str):
        self._log(f"USER_INPUT: {expression}")
        try:
            parsed = ast.parse(expression, mode="eval")
            return self._evaluate_ast(parsed.body)
        except Exception:
            raise ValueError("Invalid or unsupported expression.")

    def _evaluate_ast(self, node):
        # Python 3.8+: ast.Constant replaces ast.Num
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError("Unsupported constant type.")

        # older Python versions
        if hasattr(ast, "Num") and isinstance(node, ast.Num):
            return node.n

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in self.OPS:
                raise ValueError("Unsupported operator.")
            return self.OPS[op_type](
                self._evaluate_ast(node.left),
                self._evaluate_ast(node.right)
            )

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in self.OPS:
                raise ValueError("Unsupported unary operator.")
            return self.OPS[op_type](self._evaluate_ast(node.operand))

        raise ValueError("Unsupported expression.")
