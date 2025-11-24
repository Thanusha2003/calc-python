# test_secure_calculator.py

import unittest
from secure_calculator import SecureCalculator


class TestSecureCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = SecureCalculator(log_file="test_log.txt")

    def test_addition(self):
        self.assertEqual(self.calc.evaluate("2 + 3"), 5)

    def test_subtraction(self):
        self.assertEqual(self.calc.evaluate("10 - 4"), 6)

    def test_multiplication(self):
        self.assertEqual(self.calc.evaluate("3 * 4"), 12)

    def test_division(self):
        self.assertEqual(self.calc.evaluate("12 / 3"), 4)

    def test_power(self):
        self.assertEqual(self.calc.evaluate("2 ** 3"), 8)

    def test_modulus(self):
        self.assertEqual(self.calc.evaluate("10 % 3"), 1)

    def test_floor_division(self):
        self.assertEqual(self.calc.evaluate("10 // 3"), 3)

    def test_unary_negative(self):
        self.assertEqual(self.calc.evaluate("-5"), -5)

    def test_parentheses(self):
        self.assertEqual(self.calc.evaluate("(2 + 3) * 4"), 20)

    def test_invalid_expression(self):
        with self.assertRaises(ValueError):
            self.calc.evaluate("2 + ")

    def test_unsupported_operator(self):
        with self.assertRaises(ValueError):
            self.calc.evaluate("2 & 3")  # Bitwise ops not allowed

    def test_no_function_calls(self):
        with self.assertRaises(ValueError):
            self.calc.evaluate("__import__('os').system('ls')")

    def test_no_variable_access(self):
        with self.assertRaises(ValueError):
            self.calc.evaluate("a + 1")  # No variable names allowed


if __name__ == "__main__":
    unittest.main()
