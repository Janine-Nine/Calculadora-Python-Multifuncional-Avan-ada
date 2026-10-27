"""
Testes de matemática financeira com precisão Decimal e formatação brasileira.
"""

from decimal import Decimal
import unittest
from app.finance import FinanceEngine, format_brl
from app.validators import MathDomainError


class TestFinanceEngine(unittest.TestCase):

    def test_brl_formatting(self):
        self.assertEqual(format_brl(1250.5), "R$ 1.250,50")
        self.assertEqual(format_brl(0), "R$ 0,00")
        self.assertEqual(format_brl(1000000), "R$ 1.000.000,00")
        self.assertEqual(format_brl(-50.25), "-R$ 50,25")

    def test_simple_interest(self):
        # C = 1000, i = 2% ao mês, t = 6 meses => J = 120, M = 1120
        res = FinanceEngine.simple_interest(1000, 2, 6)
        self.assertEqual(res["juros"], Decimal("120.00"))
        self.assertEqual(res["montante"], Decimal("1120.00"))

    def test_compound_interest(self):
        # C = 1000, i = 10% a.a., t = 2 anos => M = 1000 * 1.21 = 1210
        res = FinanceEngine.compound_interest(1000, 10, 2)
        self.assertEqual(res["montante"], Decimal("1210.00"))
        self.assertEqual(res["juros"], Decimal("210.00"))

    def test_rate_conversion(self):
        # 1% ao mês -> anual (1.01^12 - 1) ≈ 12.6825%
        res = FinanceEngine.convert_interest_rate(1.0, "mensal", "anual")
        self.assertAlmostEqual(res["taxa_convertida_pct"], 12.6825, places=3)

    def test_price_financing(self):
        # R$ 10.000 financiado em 24x com 1.5% ao mês
        res = FinanceEngine.price_table_financing(10000, 1.5, 24)
        self.assertEqual(res["parcelas_total"], 24)
        # Parcela Price exata esperada em torno de R$ 499,24
        self.assertTrue(490 < float(res["valor_parcela"]) < 510)
        self.assertTrue(res["total_pago"] > Decimal("10000.00"))

    def test_margin_and_markup(self):
        # Custo 50, Venda 100 => Lucro 50, Margem 50%, Markup 100%
        res = FinanceEngine.margin_and_markup(50, 100)
        self.assertEqual(res["lucro_bruto"], Decimal("50.00"))
        self.assertEqual(res["margem_lucro_pct"], Decimal("50.00"))
        self.assertEqual(res["markup_pct"], Decimal("100.00"))

    def test_price_from_desired_margin(self):
        # Custo 80, Margem desejada 20% => Preço = 80 / 0.8 = 100
        res = FinanceEngine.price_from_desired_margin(80, 20)
        self.assertEqual(res["preco_sugerido"], Decimal("100.00"))

    def test_invalid_margin_over_100(self):
        with self.assertRaises(MathDomainError):
            FinanceEngine.price_from_desired_margin(100, 100)


if __name__ == "__main__":
    unittest.main()
