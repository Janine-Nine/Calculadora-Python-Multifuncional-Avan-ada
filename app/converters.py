"""
Módulo de Conversão de Unidades
Implementa 11 categorias de conversão física, científica e computacional.
Diferencia explicitamente unidades decimais (MB) de binárias (MiB).
"""

import math
from typing import Dict, Any, List
from app.validators import validate_number, ValidationError, MathDomainError


class UnitConverter:
    """Conversor universal de grandezas e unidades com alta precisão."""

    # Fatores lineares relativos à unidade base (SI)
    LENGTH_FACTORS = {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1.0,
        "km": 1000.0,
        "in": 0.0254,          # polegadas
        "ft": 0.3048,          # pés
        "yd": 0.9144,          # jardas
        "mi": 1609.344,        # milhas
    }

    MASS_FACTORS = {
        "mg": 0.000001,
        "g": 0.001,
        "kg": 1.0,
        "t": 1000.0,           # toneladas métricas
        "oz": 0.028349523125,  # onças
        "lb": 0.45359237,      # libras
    }

    TIME_FACTORS = {
        "ms": 0.001,
        "s": 1.0,
        "min": 60.0,
        "h": 3600.0,
        "d": 86400.0,
        "sem": 604800.0,       # semanas
    }

    AREA_FACTORS = {
        "mm2": 1e-6,
        "cm2": 1e-4,
        "m2": 1.0,
        "ha": 10000.0,         # hectare
        "km2": 1e6,
    }

    VOLUME_FACTORS = {
        "ml": 0.001,
        "l": 1.0,
        "m3": 1000.0,
        "gal": 3.785411784,     # galão americano líquido
    }

    SPEED_FACTORS = {
        "m/s": 1.0,
        "km/h": 1.0 / 3.6,
        "mph": 0.44704,
    }

    DIGITAL_FACTORS = {
        # Unidade base: byte (B)
        "bit": 1.0 / 8.0,
        "B": 1.0,
        # Padrão Decimal SI (10^n)
        "KB": 1000.0,
        "MB": 1000.0 ** 2,
        "GB": 1000.0 ** 3,
        "TB": 1000.0 ** 4,
        # Padrão Binário IEC (2^n)
        "KiB": 1024.0,
        "MiB": 1024.0 ** 2,
        "GiB": 1024.0 ** 3,
        "TiB": 1024.0 ** 4,
    }

    ENERGY_FACTORS = {
        "J": 1.0,
        "kJ": 1000.0,
        "cal": 4.184,
        "kcal": 4184.0,
        "kWh": 3600000.0,
    }

    PRESSURE_FACTORS = {
        "Pa": 1.0,
        "kPa": 1000.0,
        "bar": 100000.0,
        "atm": 101325.0,
        "psi": 6894.757293,
    }

    ANGLE_FACTORS = {
        "deg": 1.0,
        "rad": 180.0 / math.pi,
        "grad": 0.9,
    }

    @classmethod
    def convert_length(cls, val: float, from_u: str, to_u: str) -> float:
        v = validate_number(val, "Comprimento")
        if from_u not in cls.LENGTH_FACTORS or to_u not in cls.LENGTH_FACTORS:
            raise ValidationError(f"Unidade de comprimento não suportada: '{from_u}' ou '{to_u}'.")
        # Converte para base (metros) e depois para destino
        base = v * cls.LENGTH_FACTORS[from_u]
        return base / cls.LENGTH_FACTORS[to_u]

    @classmethod
    def convert_mass(cls, val: float, from_u: str, to_u: str) -> float:
        v = validate_number(val, "Massa")
        if v < 0:
            raise MathDomainError("Massa física não pode ser negativa.")
        if from_u not in cls.MASS_FACTORS or to_u not in cls.MASS_FACTORS:
            raise ValidationError(f"Unidade de massa não suportada: '{from_u}' ou '{to_u}'.")
        base = v * cls.MASS_FACTORS[from_u]
        return base / cls.MASS_FACTORS[to_u]

    @classmethod
    def convert_temperature(cls, val: float, from_u: str, to_u: str) -> float:
        v = validate_number(val, "Temperatura")
        from_u = from_u.upper()
        to_u = to_u.upper()

        # Valida zero absoluto
        if from_u == "K" and v < 0:
            raise MathDomainError("Temperatura em Kelvin não pode ser inferior ao zero absoluto (0 K).")
        if from_u == "C" and v < -273.15:
            raise MathDomainError("Temperatura em Celsius não pode ser inferior ao zero absoluto (-273.15 °C).")
        if from_u == "F" and v < -459.67:
            raise MathDomainError("Temperatura em Fahrenheit não pode ser inferior ao zero absoluto (-459.67 °F).")

        # Converte primeiro para Celsius
        if from_u == "C":
            celsius = v
        elif from_u == "F":
            celsius = (v - 32.0) * (5.0 / 9.0)
        elif from_u == "K":
            celsius = v - 273.15
        else:
            raise ValidationError(f"Unidade de temperatura inválida: '{from_u}'.")

        # Converte de Celsius para destino
        if to_u == "C":
            return celsius
        elif to_u == "F":
            return (celsius * (9.0 / 5.0)) + 32.0
        elif to_u == "K":
            return celsius + 273.15
        else:
            raise ValidationError(f"Unidade de temperatura inválida: '{to_u}'.")

    @classmethod
    def convert_time(cls, val: float, from_u: str, to_u: str) -> float:
        v = validate_number(val, "Tempo")
        if from_u not in cls.TIME_FACTORS or to_u not in cls.TIME_FACTORS:
            raise ValidationError(f"Unidade de tempo inválida: '{from_u}' ou '{to_u}'.")
        base = v * cls.TIME_FACTORS[from_u]
        return base / cls.TIME_FACTORS[to_u]

    @classmethod
    def convert_area(cls, val: float, from_u: str, to_u: str) -> float:
        v = validate_number(val, "Área")
        if v < 0:
            raise MathDomainError("Área física não pode ser negativa.")
        if from_u not in cls.AREA_FACTORS or to_u not in cls.AREA_FACTORS:
            raise ValidationError(f"Unidade de área inválida: '{from_u}' ou '{to_u}'.")
        base = v * cls.AREA_FACTORS[from_u]
        return base / cls.AREA_FACTORS[to_u]

    @classmethod
    def convert_volume(cls, val: float, from_u: str, to_u: str) -> float:
        v = validate_number(val, "Volume")
        if v < 0:
            raise MathDomainError("Volume físico não pode ser negativo.")
        if from_u not in cls.VOLUME_FACTORS or to_u not in cls.VOLUME_FACTORS:
            raise ValidationError(f"Unidade de volume inválida: '{from_u}' ou '{to_u}'.")
        base = v * cls.VOLUME_FACTORS[from_u]
        return base / cls.VOLUME_FACTORS[to_u]

    @classmethod
    def convert_speed(cls, val: float, from_u: str, to_u: str) -> float:
        v = validate_number(val, "Velocidade")
        if from_u not in cls.SPEED_FACTORS or to_u not in cls.SPEED_FACTORS:
            raise ValidationError(f"Unidade de velocidade inválida: '{from_u}' ou '{to_u}'.")
        base = v * cls.SPEED_FACTORS[from_u]
        return base / cls.SPEED_FACTORS[to_u]

    @classmethod
    def convert_digital_data(cls, val: float, from_u: str, to_u: str) -> float:
        v = validate_number(val, "Dados digitais")
        if v < 0:
            raise MathDomainError("Tamanho de dados digitais não pode ser negativo.")
        if from_u not in cls.DIGITAL_FACTORS or to_u not in cls.DIGITAL_FACTORS:
            raise ValidationError(f"Unidade de dados inválida: '{from_u}' ou '{to_u}'.")
        base_bytes = v * cls.DIGITAL_FACTORS[from_u]
        return base_bytes / cls.DIGITAL_FACTORS[to_u]

    @classmethod
    def convert_energy(cls, val: float, from_u: str, to_u: str) -> float:
        v = validate_number(val, "Energia")
        if from_u not in cls.ENERGY_FACTORS or to_u not in cls.ENERGY_FACTORS:
            raise ValidationError(f"Unidade de energia inválida: '{from_u}' ou '{to_u}'.")
        base_joules = v * cls.ENERGY_FACTORS[from_u]
        return base_joules / cls.ENERGY_FACTORS[to_u]

    @classmethod
    def convert_pressure(cls, val: float, from_u: str, to_u: str) -> float:
        v = validate_number(val, "Pressão")
        if from_u not in cls.PRESSURE_FACTORS or to_u not in cls.PRESSURE_FACTORS:
            raise ValidationError(f"Unidade de pressão inválida: '{from_u}' ou '{to_u}'.")
        base_pa = v * cls.PRESSURE_FACTORS[from_u]
        return base_pa / cls.PRESSURE_FACTORS[to_u]

    @classmethod
    def convert_angle(cls, val: float, from_u: str, to_u: str) -> float:
        v = validate_number(val, "Ângulo")
        if from_u not in cls.ANGLE_FACTORS or to_u not in cls.ANGLE_FACTORS:
            raise ValidationError(f"Unidade angular inválida: '{from_u}' ou '{to_u}'.")
        base_deg = v * cls.ANGLE_FACTORS[from_u]
        return base_deg / cls.ANGLE_FACTORS[to_u]
