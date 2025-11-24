# ⚠️ Extremely Vulnerable Python Calculator
# This code contains multiple intentional security vulnerabilities
# and must NOT be used in production.

import os
import datetime

print("=== VULNERABLE Python Calculator ===")
print("Type ANY Python expression and it will be executed.")
print("Example: 2 + 2")
print("You can also run system commands like: __import__('os').system('dir')\n")

# Insecure logging (sensitive data exposure)
log_file = "calc_log.txt"

while True:
    expr = input("Enter expression (or type 'exit' to quit): ")

    if expr.lower() == "exit":
        print("Goodbye!")
        break

    # Log input without sanitizing — vulnerable to log injection
    with open(log_file, "a") as f:
        f.write(f"{datetime.datetime.now()} - USER INPUT: {expr}\n")

    try:
        # CRITICAL VULNERABILITY: eval() executes arbitrary code
        result = eval(expr)

        print("Result:", result)

    except Exception as e:
        # Leaks internal error details to the user (information disclosure)
        print("Error occurred:", e)
