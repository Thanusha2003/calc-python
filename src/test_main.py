import unittest
from unittest.mock import patch
from io import StringIO
import builtins

# Import the vulnerable code by placing it into a function.
# Modify your vulnerable calculator file so the logic is inside a function:
#
# def run_calculator():
#     ...  (your vulnerable code)
#
# Then import it:
#
# from vulnerable_calculator import run_calculator
#
# For demonstration, I will test the core eval behavior directly.


class TestVulnerableCalculator(unittest.TestCase):

    @patch("builtins.input", side_effect=["2 + 2", "exit"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_basic_addition(self, mock_stdout, mock_input):
        """Test simple expression evaluation."""
        from vulnerable_calculator import run_calculator
        run_calculator()

        output = mock_stdout.getvalue()
        self.assertIn("Result: 4", output)

    @patch("builtins.input", side_effect=["10 * 5", "exit"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_multiplication(self, mock_stdout, mock_input):
        from vulnerable_calculator import run_calculator
        run_calculator()

        output = mock_stdout.getvalue()
        self.assertIn("Result: 50", output)

    @patch("builtins.input", side_effect=["1 / 0", "exit"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_division_by_zero(self, mock_stdout, mock_input):
        from vulnerable_calculator import run_calculator
        run_calculator()

        output = mock_stdout.getvalue()
        self.assertIn("Error occurred:", output)

    @patch("builtins.input", side_effect=["__import__('os').system('echo hacked')", "exit"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_code_execution(self, mock_stdout, mock_input):
        """Confirms that eval executes arbitrary code (vulnerability demonstration)."""
        from vulnerable_calculator import run_calculator
        run_calculator()

        output = mock_stdout.getvalue()
        # Command output appears in stdout
        self.assertIn("hacked", output)


if __name__ == "__main__":
    unittest.main()
