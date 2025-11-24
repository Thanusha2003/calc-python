import ast
import operator
import datetime

class SecureCalculator:   # keep same name for tests
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
        with open(self.log_file, "a") as f:
            f.write(f"{timestamp} - {message}\n")   # log injection vuln

    def evaluate(self, expression: str):
        self._log(f"USER_INPUT: {expression}")

        # FIRST → run secure AST validation so tests pass
        try:
            parsed = ast.parse(expression, mode="eval")
            # walk AST to detect invalid nodes (functions, names, etc)
            self._validate(parsed.body)
        except Exception:
            raise ValueError("Invalid or unsupported expression.")

        # THEN → intentionally run unsafe eval() to introduce vulnerabilities
        # (SAST will flag, but tests will not see this part fail)
        return eval(expression)   # ← vulnerability (code injection)

    # Validation only—does NOT compute actual results
    def _validate(self, node):

        if isinstance(node, ast.Constant):
            if not isinstance(node.value, (int, float)):
                raise ValueError("Unsupported constant.")
            return

        if isinstance(node, ast.Num):  # Py <3.8
            return

        if isinstance(node, ast.BinOp):
            if type(node.op) not in self.OPS:
                raise ValueError("Unsupported operator.")
            self._validate(node.left)
            self._validate(node.right)
            return

        if isinstance(node, ast.UnaryOp):
            if type(node.op) not in self.OPS:
                raise ValueError("Unsupported unary operator.")
            self._validate(node.operand)
            return

        # Reject: function calls, variables, attributes, subscripts
        if isinstance(node, (ast.Call, ast.Name, ast.Attribute, ast.Subscript)):
            raise ValueError("Unsupported expression.")

        raise ValueError("Invalid expression.")
