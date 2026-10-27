"""
Testes dos conversores de grandezas físicas e distinção entre MB e MiB.
"""

import unittest
from app.converters import UnitConverter
from app.validators import MathDomainError


class TestUnitConverter(unittest.TestCase):

    def test_length_conversion(self):
        # 1 km = 1000 m
        self.assertAlmostEqual(UnitConverter.convert_length(1, "km", "m"), 1000.0)
        # 1 polegada = 2.54 cm
        self.assertAlmostEqual(UnitConverter.convert_length(1, "in", "cm"), 2.54)

    def test_temperature_conversion(self):
        # 0 °C = 32 °F
        self.assertAlmostEqual(UnitConverter.convert_temperature(0, "C", "F"), 32.0)
        # 100 °C = 212 °F
        self.assertAlmostEqual(UnitConverter.convert_temperature(100, "C", "F"), 212.0)
        # 0 K = -273.15 °C
        self.assertAlmostEqual(UnitConverter.convert_temperature(0, "K", "C"), -273.15)

    def test_absolute_zero_validation(self):
        with self.assertRaises(MathDomainError):
            UnitConverter.convert_temperature(-1, "K", "C")
        with self.assertRaises(MathDomainError):
            UnitConverter.convert_temperature(-300, "C", "K")

    def test_digital_data_mb_vs_mib(self):
        # 1 MB = 1.000.000 Bytes
        self.assertEqual(UnitConverter.convert_digital_data(1, "MB", "B"), 1000000.0)
        # 1 MiB = 1.048.576 Bytes (1024²)
        self.assertEqual(UnitConverter.convert_digital_data(1, "MiB", "B"), 1048576.0)
        # Proporção 1 MiB em MB: 1.048576 MB
        self.assertAlmostEqual(UnitConverter.convert_digital_data(1, "MiB", "MB"), 1.048576)

    def test_time_conversion(self):
        # 1 hora = 3600 segundos
        self.assertEqual(UnitConverter.convert_time(1, "h", "s"), 3600.0)
        # 1 dia = 24 horas
        self.assertEqual(UnitConverter.convert_time(1, "d", "h"), 24.0)


if __name__ == "__main__":
    unittest.main()
