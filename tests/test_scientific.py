"""
Testes das funções científicas avançadas e seus domínios matemáticos.
"""

import math
import unittest
from app.scientific import ScientificCalculator
from app.validators import MathDomainError


class TestScientificCalculator(unittest.TestCase):

    def test_trigonometry_degrees(self):
        self.assertAlmostEqual(ScientificCalculator.sin(0, "deg"), 0.0)
        self.assertAlmostEqual(ScientificCalculator.sin(90, "deg"), 1.0)
        self.assertAlmostEqual(ScientificCalculator.cos(0, "deg"), 1.0)
        self.assertAlmostEqual(ScientificCalculator.cos(90, "deg"), 0.0)
        self.assertAlmostEqual(ScientificCalculator.tan(45, "deg"), 1.0)

    def test_trigonometry_radians(self):
        self.assertAlmostEqual(ScientificCalculator.sin(math.pi / 2, "rad"), 1.0)
        self.assertAlmostEqual(ScientificCalculator.cos(math.pi, "rad"), -1.0)

    def test_inverse_trigonometry(self):
        self.assertAlmostEqual(ScientificCalculator.asin(1.0, "deg"), 90.0)
        self.assertAlmostEqual(ScientificCalculator.acos(1.0, "deg"), 0.0)
        self.assertAlmostEqual(ScientificCalculator.atan(1.0, "deg"), 45.0)

        with self.assertRaises(MathDomainError):
            ScientificCalculator.asin(2.0)

    def test_logarithms(self):
        self.assertAlmostEqual(ScientificCalculator.log10(1000), 3.0)
        self.assertAlmostEqual(ScientificCalculator.ln(math.e ** 2), 2.0)
        self.assertAlmostEqual(ScientificCalculator.log_base(16, 2), 4.0)

        with self.assertRaises(MathDomainError):
            ScientificCalculator.log_base(10, 1)  # Base 1 não permitida

    def test_combinatorics(self):
        # Fatorial
        self.assertEqual(ScientificCalculator.factorial(5), 120)
        self.assertEqual(ScientificCalculator.factorial(0), 1)

        # Combinação C(5, 2) = 10
        self.assertEqual(ScientificCalculator.combination(5, 2), 10)
        # Permutação P(5, 2) = 20
        self.assertEqual(ScientificCalculator.permutation(5, 2), 20)

        with self.assertRaises(MathDomainError):
            ScientificCalculator.combination(3, 5)

    def test_nth_root(self):
        self.assertAlmostEqual(ScientificCalculator.nth_root(27, 3), 3.0)
        self.assertAlmostEqual(ScientificCalculator.nth_root(16, 4), 2.0)
        # Raiz ímpar de negativo é real
        self.assertAlmostEqual(ScientificCalculator.nth_root(-8, 3), -2.0)
        # Raiz par de negativo não é real
        with self.assertRaises(MathDomainError):
            ScientificCalculator.nth_root(-16, 2)


if __name__ == "__main__":
    unittest.main()
