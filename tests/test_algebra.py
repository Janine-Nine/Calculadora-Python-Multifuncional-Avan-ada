"""
Testes de álgebra: equações lineares, quadráticas e sistemas 2x2.
"""

import unittest
from app.algebra import AlgebraSolver
from app.validators import ValidationError


class TestAlgebraSolver(unittest.TestCase):

    def test_solve_linear(self):
        # 2x + 4 = 10 => 2x = 6 => x = 3
        res = AlgebraSolver.solve_linear_equation(2, 4, 10)
        self.assertEqual(res["tipo"], "determinada")
        self.assertEqual(res["x"], 3.0)

    def test_quadratic_distinct_real_roots(self):
        # x² - 5x + 6 = 0 => Delta = 25 - 24 = 1 => x1=3, x2=2
        res = AlgebraSolver.solve_quadratic_equation(1, -5, 6)
        self.assertEqual(res["tipo"], "reais_distintas")
        self.assertEqual(res["delta"], 1.0)
        self.assertAlmostEqual(res["x1"], 3.0)
        self.assertAlmostEqual(res["x2"], 2.0)

    def test_quadratic_double_real_root(self):
        # x² - 4x + 4 = 0 => Delta = 0 => x = 2
        res = AlgebraSolver.solve_quadratic_equation(1, -4, 4)
        self.assertEqual(res["tipo"], "real_dupla")
        self.assertEqual(res["delta"], 0.0)
        self.assertAlmostEqual(res["x1"], 2.0)

    def test_quadratic_complex_roots(self):
        # x² + 1 = 0 => a=1, b=0, c=1 => Delta = -4 => raízes complexas ±1i
        res = AlgebraSolver.solve_quadratic_equation(1, 0, 1)
        self.assertEqual(res["tipo"], "complexas")
        self.assertEqual(res["delta"], -4.0)
        self.assertEqual(res["real"], 0.0)
        self.assertAlmostEqual(res["imag"], 1.0)

    def test_linear_system_spd(self):
        # x + y = 10 e x - y = 2 => x = 6, y = 4
        res = AlgebraSolver.solve_linear_system_2x2(1, 1, 10, 1, -1, 2)
        self.assertEqual(res["classificacao"], "SPD")
        self.assertAlmostEqual(res["x"], 6.0)
        self.assertAlmostEqual(res["y"], 4.0)

    def test_linear_system_si(self):
        # Retas paralelas distintas: x + y = 5 e x + y = 8
        res = AlgebraSolver.solve_linear_system_2x2(1, 1, 5, 1, 1, 8)
        self.assertEqual(res["classificacao"], "SI")
        self.assertIsNone(res["x"])

    def test_linear_system_spi(self):
        # Retas coincidentes: x + y = 5 e 2x + 2y = 10
        res = AlgebraSolver.solve_linear_system_2x2(1, 1, 5, 2, 2, 10)
        self.assertEqual(res["classificacao"], "SPI")
        self.assertIsNone(res["x"])


if __name__ == "__main__":
    unittest.main()
