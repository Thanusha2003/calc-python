# secure_calculator.py

import ast
import operator
import datetime

class SecureCalculator:
    """A safe calculator that evaluates basic math expressions without using eval()."""

    # Supported operators
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
        """Safe logging without exposing user-controlled raw content."""
        timestamp = datetime.datetime.now().isoformat()
        safe_message = message.replace("\n", "\\n")  # prevent log injection
        with open(self.log_file, "a") as f:
            f.write(f"{timestamp} - {safe_message}\n")

    def evaluate(self, expression: str):
        """Safely evaluate a math expression."""
        self._log(f"USER_INPUT: {expression}")

        try:
            parsed = ast.parse(expression, mode="eval")
            return self._evaluate_ast(parsed.body)
        except Exception:
            raise ValueError("Invalid or unsupported expression.")

    def _evaluate_ast(self, node):
        """Recursively evaluate allowed AST nodes."""
        if isinstance(node, ast.Num):  # numbers
            return node.n
        if isinstance(node, ast.BinOp):  # binary operations
            op_type = type(node.op)
            if op_type not in self.OPS:
                raise ValueError("Unsupported operator.")
            return self.OPS[op_type](
                self._evaluate_ast(node.left),
                self._evaluate_ast(node.right)
            )
        if isinstance(node, ast.UnaryOp):  # unary operations
            op_type = type(node.op)
            if op_type not in self.OPS:
                raise ValueError("Unsupported unary operator.")
            return self.OPS[op_type](self._evaluate_ast(node.operand))

        raise ValueError("Unsupported expression type.")


def main():
    calc = SecureCalculator()

    print("=== Secure Python Calculator ===")
    print("Supports: +, -, *, /, %, //, **")
    print("Type 'exit' to quit.\n")

    while True:
        expr = input("Enter expression: ")

        if expr.lower() == "exit":
            print("Goodbye!")
            break

        try:
            result = calc.evaluate(expr)
            print("Result:", result)
        except ValueError as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
