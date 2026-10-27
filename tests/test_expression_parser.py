"""
Testes do Interpretador Matemático Seguro (Safe Expression Parser).
Verifica tokenização, precedência, parênteses, funções autorizadas,
tratamento de erros sintáticos e proteção estrita contra injeção de código.
"""

import math
import unittest
from app.expression_parser import SafeExpressionParser
from app.validators import ValidationError, MathDomainError


class TestSafeExpressionParser(unittest.TestCase):

    def setUp(self):
        self.parser = SafeExpressionParser(angle_mode="deg")

    def test_basic_arithmetic(self):
        self.assertEqual(self.parser.evaluate("2 + 3"), 5)
        self.assertEqual(self.parser.evaluate("10 - 4"), 6)
        self.assertEqual(self.parser.evaluate("3 * 7"), 21)
        self.assertEqual(self.parser.evaluate("15 / 3"), 5)

    def test_operator_precedence(self):
        # Multiplicação antes da adição
        self.assertEqual(self.parser.evaluate("2 + 3 * 4"), 14)
        # Parênteses alteram a ordem
        self.assertEqual(self.parser.evaluate("(2 + 3) * 4"), 20)
        # Divisão e exponenciação
        self.assertEqual(self.parser.evaluate("2 * 3 ^ 2"), 18)

    def test_decimal_comma_and_dot(self):
        # Suporte ao separador brasileiro de vírgula entre números
        self.assertAlmostEqual(self.parser.evaluate("2,5 + 3,5"), 6.0)
        self.assertAlmostEqual(self.parser.evaluate("2.5 + 3.5"), 6.0)

    def test_unary_signs(self):
        self.assertEqual(self.parser.evaluate("-5 + 10"), 5)
        self.assertEqual(self.parser.evaluate("-(2 + 3)"), -5)
        self.assertEqual(self.parser.evaluate("+8 - -2"), 10)

    def test_factorial(self):
        self.assertEqual(self.parser.evaluate("5!"), 120)
        self.assertEqual(self.parser.evaluate("0!"), 1)
        self.assertEqual(self.parser.evaluate("3! + 4!"), 30)

    def test_authorized_constants(self):
        self.assertAlmostEqual(self.parser.evaluate("pi"), math.pi)
        self.assertAlmostEqual(self.parser.evaluate("e"), math.e)

    def test_authorized_functions(self):
        self.assertAlmostEqual(self.parser.evaluate("sqrt(16)"), 4.0)
        self.assertAlmostEqual(self.parser.evaluate("abs(-42)"), 42)
        self.assertAlmostEqual(self.parser.evaluate("sin(90)"), 1.0)
        self.assertAlmostEqual(self.parser.evaluate("cos(0)"), 1.0)
        self.assertAlmostEqual(self.parser.evaluate("log10(100)"), 2.0)
        self.assertAlmostEqual(self.parser.evaluate("ln(e)"), 1.0)

    def test_division_by_zero(self):
        with self.assertRaises(MathDomainError):
            self.parser.evaluate("10 / 0")

    def test_negative_square_root(self):
        with self.assertRaises(MathDomainError):
            self.parser.evaluate("sqrt(-9)")

    def test_log_zero_or_negative(self):
        with self.assertRaises(MathDomainError):
            self.parser.evaluate("log10(0)")
        with self.assertRaises(MathDomainError):
            self.parser.evaluate("ln(-5)")

    def test_security_rejection_of_python_code(self):
        # Tentativas de injeção de código, funções embutidas e comandos de sistema
        malicious_inputs = [
            "__import__('os').system('ls')",
            "open('/etc/passwd').read()",
            "eval('2+2')",
            "exec('import sys')",
            "lambda x: x+1",
            "globals()",
            "locals()",
            "getattr(math, 'sin')",
        ]
        for payload in malicious_inputs:
            with self.assertRaises(ValidationError, msg=f"Falha de segurança ao rejeitar: {payload}"):
                self.parser.evaluate(payload)

    def test_syntax_errors(self):
        with self.assertRaises(ValidationError):
            self.parser.evaluate("(2 + 3")
        with self.assertRaises(ValidationError):
            self.parser.evaluate("2 + * 3")
        with self.assertRaises(ValidationError):
            self.parser.evaluate("")


if __name__ == "__main__":
    unittest.main()
