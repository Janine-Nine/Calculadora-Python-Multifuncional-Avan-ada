"""
Módulo de Funções Científicas Avançadas
Implementa trigonometria, logaritmos, combinatória, potências, raízes e funções hiperbólicas.
"""

import math
from typing import Union
from app.validators import (
    validate_number,
    validate_non_negative,
    validate_positive,
    validate_non_negative_integer,
    MathDomainError,
)


class ScientificCalculator:
    """Implementação orientada a objetos de funções matemáticas científicas."""

    @staticmethod
    def to_radians(angle_degrees: float) -> float:
        return math.radians(angle_degrees)

    @staticmethod
    def to_degrees(angle_radians: float) -> float:
        return math.degrees(angle_radians)

    @staticmethod
    def sin(x: float, angle_mode: str = "deg") -> float:
        val = validate_number(x, "Ângulo")
        rad = math.radians(val) if angle_mode.lower() == "deg" else val
        res = math.sin(rad)
        return 0.0 if abs(res) < 1e-15 else res

    @staticmethod
    def cos(x: float, angle_mode: str = "deg") -> float:
        val = validate_number(x, "Ângulo")
        rad = math.radians(val) if angle_mode.lower() == "deg" else val
        res = math.cos(rad)
        return 0.0 if abs(res) < 1e-15 else res

    @staticmethod
    def tan(x: float, angle_mode: str = "deg") -> float:
        val = validate_number(x, "Ângulo")
        rad = math.radians(val) if angle_mode.lower() == "deg" else val
        cos_val = math.cos(rad)
        if abs(cos_val) < 1e-15:
            raise MathDomainError("Tangente indefinida: cosseno nulo / assíntota vertical.")
        res = math.tan(rad)
        return 0.0 if abs(res) < 1e-15 else res

    @staticmethod
    def asin(x: float, angle_mode: str = "deg") -> float:
        val = validate_number(x, "Valor")
        if val < -1.0 or val > 1.0:
            raise MathDomainError("Arco-seno definido apenas no intervalo [-1, 1].")
        res = math.asin(val)
        return math.degrees(res) if angle_mode.lower() == "deg" else res

    @staticmethod
    def acos(x: float, angle_mode: str = "deg") -> float:
        val = validate_number(x, "Valor")
        if val < -1.0 or val > 1.0:
            raise MathDomainError("Arco-cosseno definido apenas no intervalo [-1, 1].")
        res = math.acos(val)
        return math.degrees(res) if angle_mode.lower() == "deg" else res

    @staticmethod
    def atan(x: float, angle_mode: str = "deg") -> float:
        val = validate_number(x, "Valor")
        res = math.atan(val)
        return math.degrees(res) if angle_mode.lower() == "deg" else res

    @staticmethod
    def ln(x: float) -> float:
        val = validate_positive(x, "Logaritmando")
        return math.log(val)

    @staticmethod
    def log10(x: float) -> float:
        val = validate_positive(x, "Logaritmando")
        return math.log10(val)

    @staticmethod
    def log_base(x: float, base: float) -> float:
        val = validate_positive(x, "Logaritmando")
        b = validate_positive(base, "Base do logaritmo")
        if b == 1.0:
            raise MathDomainError("A base do logaritmo não pode ser igual a 1.")
        return math.log(val, b)

    @staticmethod
    def exp(x: float) -> float:
        val = validate_number(x, "Expoente")
        if val > 700:
            raise MathDomainError("Expoente excessivo para exp(x); limite flutuante excedido.")
        return math.exp(val)

    @staticmethod
    def power(base: float, exponent: float) -> float:
        b = validate_number(base, "Base")
        exp_val = validate_number(exponent, "Expoente")
        if b < 0 and not float(exp_val).is_integer():
            raise MathDomainError("Base negativa com expoente não-inteiro não possui raiz real.")
        try:
            return b ** exp_val
        except OverflowError as err:
            raise MathDomainError("Estouro de capacidade numérica na potenciação.") from err

    @staticmethod
    def nth_root(value: float, n: int) -> float:
        val = validate_number(value, "Radicando")
        index = validate_non_negative_integer(n, "Índice da raiz")
        if index == 0:
            raise MathDomainError("Índice da raiz não pode ser zero.")
        if val < 0:
            if index % 2 == 0:
                raise MathDomainError("Raiz de índice par para radicando negativo não pertence aos reais.")
            return -((-val) ** (1.0 / index))
        return val ** (1.0 / index)

    @staticmethod
    def factorial(n: int) -> int:
        val = validate_non_negative_integer(n, "Número para fatorial", max_limit=170)
        return math.factorial(val)

    @staticmethod
    def permutation(n: int, k: int) -> int:
        n_val = validate_non_negative_integer(n, "Total de elementos (n)", max_limit=170)
        k_val = validate_non_negative_integer(k, "Elementos escolhidos (k)", max_limit=170)
        if k_val > n_val:
            raise MathDomainError(f"k ({k_val}) não pode ser maior que n ({n_val}) em permutações.")
        return math.perm(n_val, k_val)

    @staticmethod
    def combination(n: int, k: int) -> int:
        n_val = validate_non_negative_integer(n, "Total de elementos (n)", max_limit=170)
        k_val = validate_non_negative_integer(k, "Elementos escolhidos (k)", max_limit=170)
        if k_val > n_val:
            raise MathDomainError(f"k ({k_val}) não pode ser maior que n ({n_val}) em combinações.")
        return math.comb(n_val, k_val)

    @staticmethod
    def sinh(x: float) -> float:
        return math.sinh(validate_number(x, "x"))

    @staticmethod
    def cosh(x: float) -> float:
        return math.cosh(validate_number(x, "x"))

    @staticmethod
    def tanh(x: float) -> float:
        return math.tanh(validate_number(x, "x"))

    @staticmethod
    def floor(x: float) -> int:
        return math.floor(validate_number(x, "x"))

    @staticmethod
    def ceil(x: float) -> int:
        return math.ceil(validate_number(x, "x"))

    @staticmethod
    def trunc(x: float) -> int:
        return math.trunc(validate_number(x, "x"))

    @staticmethod
    def round_precision(x: float, decimals: int = 4) -> float:
        val = validate_number(x, "Valor")
        dec = validate_non_negative_integer(decimals, "Casas decimais", max_limit=20)
        return round(val, dec)

    @staticmethod
    def format_scientific(x: float, precision: int = 4) -> str:
        val = validate_number(x, "Valor")
        return f"{val:.{precision}e}"
