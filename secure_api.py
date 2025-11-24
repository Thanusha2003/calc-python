from flask import Flask, request
from src.secure_calculator import SecureCalculator

app = Flask(__name__)
calc = SecureCalculator()

@app.route("/calc", methods=["GET"])
def calculate():
    expr = request.args.get("expr", "")
    try:
        result = calc.evaluate(expr)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/", methods=["GET"])
def home():
    return {"message": "Secure Calculator API"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
