"""
Módulo de Frações e Aritmética Exata
Implementa simplificação, operações exatas, conversão decimal, MDC, MMC,
primalidade, fatoração prima e lista de divisores.
"""

import math
from fractions import Fraction
from typing import List, Tuple, Dict
from app.validators import (
    validate_integer,
    validate_positive,
    validate_non_zero,
    validate_number,
    ValidationError,
    MathDomainError,
)


class FractionsMath:
    """Ferramentas de aritmética e teoria dos números com representação exata."""

    @staticmethod
    def simplify_fraction(numerator: int, denominator: int) -> Tuple[int, int]:
        num = validate_integer(numerator, "Numerador")
        den = validate_integer(denominator, "Denominador")
        if den == 0:
            raise MathDomainError("Denominador de uma fração não pode ser zero.")
        f = Fraction(num, den)
        return f.numerator, f.denominator

    @staticmethod
    def add_fractions(n1: int, d1: int, n2: int, d2: int) -> Tuple[int, int]:
        f1 = Fraction(validate_integer(n1, "N1"), validate_non_zero(d1, "D1"))
        f2 = Fraction(validate_integer(n2, "N2"), validate_non_zero(d2, "D2"))
        res = f1 + f2
        return res.numerator, res.denominator

    @staticmethod
    def subtract_fractions(n1: int, d1: int, n2: int, d2: int) -> Tuple[int, int]:
        f1 = Fraction(validate_integer(n1, "N1"), validate_non_zero(d1, "D1"))
        f2 = Fraction(validate_integer(n2, "N2"), validate_non_zero(d2, "D2"))
        res = f1 - f2
        return res.numerator, res.denominator

    @staticmethod
    def multiply_fractions(n1: int, d1: int, n2: int, d2: int) -> Tuple[int, int]:
        f1 = Fraction(validate_integer(n1, "N1"), validate_non_zero(d1, "D1"))
        f2 = Fraction(validate_integer(n2, "N2"), validate_non_zero(d2, "D2"))
        res = f1 * f2
        return res.numerator, res.denominator

    @staticmethod
    def divide_fractions(n1: int, d1: int, n2: int, d2: int) -> Tuple[int, int]:
        f1 = Fraction(validate_integer(n1, "N1"), validate_non_zero(d1, "D1"))
        f2 = Fraction(validate_integer(n2, "N2"), validate_non_zero(d2, "D2"))
        if f2.numerator == 0:
            raise MathDomainError("Divisão por fração nula não permitida.")
        res = f1 / f2
        return res.numerator, res.denominator

    @staticmethod
    def fraction_to_decimal(numerator: int, denominator: int) -> float:
        num = validate_integer(numerator, "Numerador")
        den = validate_non_zero(denominator, "Denominador")
        return num / den

    @staticmethod
    def decimal_to_fraction(decimal_value: float, max_denominator: int = 100000) -> Tuple[int, int]:
        val = validate_number(decimal_value, "Valor decimal")
        f = Fraction(str(val)).limit_denominator(max_denominator)
        return f.numerator, f.denominator

    @staticmethod
    def gcd_multiple(numbers: List[int]) -> int:
        if not numbers:
            raise ValidationError("Informe ao menos um número para o cálculo do MDC.")
        nums = [abs(validate_integer(n, "Elemento do MDC")) for n in numbers]
        return math.gcd(*nums)

    @staticmethod
    def lcm_two(a: int, b: int) -> int:
        if a == 0 or b == 0:
            return 0
        return abs(a * b) // math.gcd(a, b)

    @staticmethod
    def lcm_multiple(numbers: List[int]) -> int:
        if not numbers:
            raise ValidationError("Informe ao menos um número para o cálculo do MMC.")
        nums = [abs(validate_integer(n, "Elemento do MMC")) for n in numbers]
        res = nums[0]
        for n in nums[1:]:
            res = FractionsMath.lcm_two(res, n)
        return res

    @staticmethod
    def is_prime(n: int) -> bool:
        val = validate_integer(n, "Número para teste de primalidade")
        if val <= 1:
            return False
        if val <= 3:
            return True
        if val % 2 == 0 or val % 3 == 0:
            return False
        i = 5
        while i * i <= val:
            if val % i == 0 or val % (i + 2) == 0:
                return False
            i += 6
        return True

    @staticmethod
    def prime_factors(n: int) -> Dict[int, int]:
        val = validate_integer(n, "Número para fatoração prima")
        if val <= 1:
            raise MathDomainError("Fatoração prima requer número inteiro maior que 1.")
        factors: Dict[int, int] = {}
        temp = val
        d = 2
        while d * d <= temp:
            while temp % d == 0:
                factors[d] = factors.get(d, 0) + 1
                temp //= d
            d += 1 if d == 2 else 2
        if temp > 1:
            factors[temp] = factors.get(temp, 0) + 1
        return factors

    @staticmethod
    def get_divisors(n: int) -> List[int]:
        val = abs(validate_integer(n, "Número para busca de divisores"))
        if val == 0:
            raise MathDomainError("O número 0 possui infinitos divisores.")
        divs = set()
        for i in range(1, int(math.isqrt(val)) + 1):
            if val % i == 0:
                divs.add(i)
                divs.add(val // i)
        return sorted(list(divs))
