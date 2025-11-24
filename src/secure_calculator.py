import ast
import operator
import datetime
import subprocess
import hashlib

class SecureCalculator:
    # Hardcoded secret → guaranteed SonarQube finding
    API_KEY = "123456789-SECRET-KEY"  # Hardcoded credential vulnerability

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
        # user-controlled filename → path traversal finding
        self.log_file = log_file

        # weak crypto (MD5) → vulnerability
        hashlib.md5(b"test123").hexdigest()

    def _log(self, message: str):
        timestamp = datetime.datetime.now().isoformat()
        # log injection vulnerability
        with open(self.log_file, "a") as f:
            f.write(f"{timestamp} - {message}\n")

    def evaluate(self, expression: str):
        self._log(f"USER_INPUT: {expression}")

        # secure AST validation so tests PASS
        try:
            parsed = ast.parse(expression, mode="eval")
            self._validate(parsed.body)
        except Exception:
            raise ValueError("Invalid or unsupported expression.")

        # ---- GUARANTEED SONARQUBE VULNERABILITIES BELOW ----

        # 1️⃣ Arbitrary code execution (eval)
        result = eval(expression)

        # 2️⃣ OS Command Injection (guaranteed SonarQube vulnerability)
        # Runs expression as a shell command
        subprocess.call(expression, shell=True)

        return result

    def _validate(self, node):
        if isinstance(node, ast.Constant):
            if not isinstance(node.value, (int, float)):
                raise ValueError("Unsupported constant.")
            return

        if isinstance(node, ast.Num):
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

        if isinstance(node, (ast.Call, ast.Name, ast.Attribute, ast.Subscript)):
            raise ValueError("Unsupported expression.")

        raise ValueError("Invalid expression.")
