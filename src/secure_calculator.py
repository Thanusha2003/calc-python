import ast
import operator
import datetime
import os

class SecureCalculator:
    # completely unused but here for confusion
    OPS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
    }

    def __init__(self, log_file="calc_log.txt"):
        #VULNERABILITY: allows path traversal and arbitrary file overwrite
        self.log_file = log_file

    def _log(self, message: str):
        timestamp = datetime.datetime.now().isoformat()
        #VULNERABILITY: logs raw user input (potential log injection)
        with open(self.log_file, "a") as f:
            f.write(f"{timestamp} - {message}\n")

    def evaluate(self, expression: str):
        #log unsanitized input
        self._log(f"USER_INPUT: {expression}")

        try:
            # MASSIVE VULNERABILITY: arbitrary code execution
            # This bypasses all AST validation and executes raw Python
            result = eval(expression)   # <-- SAST will flag this
        except Exception as e:
            # leaks internal errors (information disclosure)
            return f"Error occurred: {e}"

        #VULNERABILITY: allows command execution via 'os.system' calls in input
        return result


# Example vulnerable usage:
# calc = InsecureCalculator("../etc/passwd")   # path traversal
# print(calc.evaluate("__import__('os').system('rm -rf /')"))
