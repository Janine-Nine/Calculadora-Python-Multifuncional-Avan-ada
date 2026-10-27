"""
Testes do motor estatístico e cálculos descritivos.
"""

import unittest
from app.statistics_tools import StatisticsEngine
from app.validators import ValidationError, MathDomainError


class TestStatisticsEngine(unittest.TestCase):

    def test_parse_series(self):
        data = StatisticsEngine.parse_data_series("10, 20.5; 30,5\n40")
        self.assertEqual(data, [10.0, 20.5, 30.5, 40.0])

    def test_descriptive_analysis(self):
        # Amostra: [2, 4, 4, 4, 5, 5, 7, 9] (n=8, soma=40, média=5)
        sample = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
        res = StatisticsEngine.descriptive_analysis(sample)

        self.assertEqual(res["n"], 8)
        self.assertEqual(res["media"], 5.0)
        self.assertEqual(res["mediana"], 4.5)
        self.assertEqual(res["modas"], [4.0])
        self.assertEqual(res["minimo"], 2.0)
        self.assertEqual(res["maximo"], 9.0)
        self.assertEqual(res["amplitude"], 7.0)
        self.assertAlmostEqual(res["variancia_populacional"], 4.0)
        self.assertAlmostEqual(res["desvio_padrao_populacional"], 2.0)

    def test_weighted_mean(self):
        vals = [8.0, 9.0, 7.0]
        weights = [2.0, 3.0, 5.0]
        # (8*2 + 9*3 + 7*5) / 10 = (16 + 27 + 35) / 10 = 78 / 10 = 7.8
        w_mean = StatisticsEngine.weighted_mean(vals, weights)
        self.assertAlmostEqual(w_mean, 7.8)

    def test_probability(self):
        # 1 dado de 6 faces: probabilidade de tirar número par (2, 4, 6) = 3/6 = 0.5
        prob = StatisticsEngine.simple_probability(3, 6)
        self.assertEqual(prob["probabilidade"], 0.5)
        self.assertEqual(prob["probabilidade_pct"], 50.0)

        with self.assertRaises(MathDomainError):
            StatisticsEngine.simple_probability(7, 6)  # Favoráveis > Total


if __name__ == "__main__":
    unittest.main()
