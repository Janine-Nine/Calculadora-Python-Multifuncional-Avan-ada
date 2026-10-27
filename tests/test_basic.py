"""
Testes das operações básicas da calculadora e gerenciamento de memória.
"""

import unittest
from app.calculator_engine import CalculatorEngine
from app.validators import MathDomainError


class TestCalculatorEngine(unittest.TestCase):

    def setUp(self):
        self.engine = CalculatorEngine()

    def test_basic_evaluation(self):
        res, raw = self.engine.evaluate_expression("15 + 25")
        self.assertEqual(raw, 40.0)

    def test_toggle_sign(self):
        self.assertEqual(CalculatorEngine.toggle_sign("42"), "-42")
        self.assertEqual(CalculatorEngine.toggle_sign("-42"), "42")
        self.assertEqual(CalculatorEngine.toggle_sign("0"), "0")

    def test_inverse(self):
        self.assertAlmostEqual(CalculatorEngine.inverse(4.0), 0.25)
        with self.assertRaises(MathDomainError):
            CalculatorEngine.inverse(0)

    def test_percentage(self):
        self.assertEqual(CalculatorEngine.percentage(20, 200), 40.0)
        self.assertEqual(CalculatorEngine.percentage(15), 0.15)

    def test_memory_operations(self):
        self.engine.memory_clear()
        self.assertEqual(self.engine.memory_recall(), 0.0)
        self.assertFalse(self.engine.has_memory)

        self.engine.memory_add(100.0)
        self.assertEqual(self.engine.memory_recall(), 100.0)
        self.assertTrue(self.engine.has_memory)

        self.engine.memory_subtract(30.0)
        self.assertEqual(self.engine.memory_recall(), 70.0)

        self.engine.memory_clear()
        self.assertEqual(self.engine.memory_recall(), 0.0)
        self.assertFalse(self.engine.has_memory)


if __name__ == "__main__":
    unittest.main()
