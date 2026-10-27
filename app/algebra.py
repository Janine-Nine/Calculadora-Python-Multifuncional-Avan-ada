"""
Módulo de Álgebra
Implementa resolução de equações de 1º e 2º grau, sistemas lineares 2x2,
produtos notáveis e fatoração de polinômios com etapas explicativas.
"""

import math
from typing import Dict, Any, Tuple, Optional
from app.validators import validate_number, ValidationError, MathDomainError


class AlgebraSolver:
    """Solucionador algébrico com passos detalhados e tratamento de casos singulares."""

    @staticmethod
    def solve_linear_equation(a: float, b: float, c: float = 0.0) -> Dict[str, Any]:
        """
        Resolve a equação linear ax + b = c => ax = c - b => x = (c - b) / a.
        """
        a_val = validate_number(a, "Coeficiente a")
        b_val = validate_number(b, "Termo b")
        c_val = validate_number(c, "Termo c")

        if a_val == 0:
            if b_val == c_val:
                return {
                    "tipo": "identidade",
                    "status": "Infinitas soluções (Identidade: 0x = 0)",
                    "passos": [
                        f"Equação: {b_val} = {c_val}",
                        "Como a = 0 e b = c, a igualdade é válida para qualquer x real.",
                    ],
                    "x": None,
                }
            return {
                "tipo": "impossivel",
                "status": "Sem solução (Equação impossível)",
                "passos": [
                    f"Equação: {a_val}x + {b_val} = {c_val}",
                    f"Resulta em: 0x = {c_val - b_val}",
                    "Impossível dividir por zero; não existe x real que satisfaça a igualdade.",
                ],
                "x": None,
            }

        diff = c_val - b_val
        x = diff / a_val

        passos = [
            f"1. Equação original: {a_val}x + ({b_val}) = {c_val}",
            f"2. Subtraindo {b_val} de ambos os lados: {a_val}x = {c_val} - ({b_val}) = {diff}",
            f"3. Dividindo ambos os lados por {a_val}: x = {diff} / {a_val} = {x}",
        ]

        return {
            "tipo": "determinada",
            "status": "Solução única encontrada",
            "x": x,
            "passos": passos,
        }

    @staticmethod
    def solve_quadratic_equation(a: float, b: float, c: float) -> Dict[str, Any]:
        """
        Resolve a equação quadrática ax² + bx + c = 0.
        Calcula o discriminante Delta e encontra raízes reais ou complexas.
        """
        a_val = validate_number(a, "Coeficiente a")
        b_val = validate_number(b, "Coeficiente b")
        c_val = validate_number(c, "Coeficiente c")

        if a_val == 0:
            raise ValidationError("O coeficiente 'a' de uma equação de 2º grau não pode ser zero.")

        # Delta = b² - 4ac
        delta = (b_val ** 2) - (4 * a_val * c_val)

        passos = [
            f"1. Equação quadrática: ({a_val})x² + ({b_val})x + ({c_val}) = 0",
            f"2. Fórmula de Bhaskara: x = (-b ± √Δ) / 2a",
            f"3. Cálculo do discriminante: Δ = b² - 4ac",
            f"   Δ = ({b_val})² - 4·({a_val})·({c_val}) = {b_val ** 2} - ({4 * a_val * c_val}) = {delta}",
        ]

        if delta > 0:
            sqrt_delta = math.sqrt(delta)
            x1 = (-b_val + sqrt_delta) / (2 * a_val)
            x2 = (-b_val - sqrt_delta) / (2 * a_val)
            passos.append(f"4. Como Δ > 0, existem duas raízes reais distintas.")
            passos.append(f"   √Δ = √{delta} = {sqrt_delta:.4f}")
            passos.append(f"   x₁ = (-({b_val}) + {sqrt_delta:.4f}) / (2·{a_val}) = {x1:.4f}")
            passos.append(f"   x₂ = (-({b_val}) - {sqrt_delta:.4f}) / (2·{a_val}) = {x2:.4f}")
            return {
                "tipo": "reais_distintas",
                "delta": delta,
                "x1": x1,
                "x2": x2,
                "x1_str": f"{x1:.6g}",
                "x2_str": f"{x2:.6g}",
                "passos": passos,
            }
        elif delta == 0:
            x = -b_val / (2 * a_val)
            passos.append(f"4. Como Δ = 0, existe uma raiz real dupla (raiz única).")
            passos.append(f"   x = -({b_val}) / (2·{a_val}) = {x:.4f}")
            return {
                "tipo": "real_dupla",
                "delta": delta,
                "x1": x,
                "x2": x,
                "x1_str": f"{x:.6g}",
                "x2_str": f"{x:.6g}",
                "passos": passos,
            }
        else:
            # Raízes complexas: p ± q i
            real_part = -b_val / (2 * a_val)
            imag_part = math.sqrt(abs(delta)) / (2 * abs(a_val))
            passos.append(f"4. Como Δ < 0 ({delta}), não existem raízes reais no domínio ℝ.")
            passos.append(f"   Existem duas raízes complexas conjugadas no conjunto ℂ:")
            passos.append(f"   x₁ = {real_part:.4f} + {imag_part:.4f}i")
            passos.append(f"   x₂ = {real_part:.4f} - {imag_part:.4f}i")
            return {
                "tipo": "complexas",
                "delta": delta,
                "real": real_part,
                "imag": imag_part,
                "x1_str": f"{real_part:.4f} + {imag_part:.4f}i",
                "x2_str": f"{real_part:.4f} - {imag_part:.4f}i",
                "passos": passos,
            }

    @staticmethod
    def solve_linear_system_2x2(
        a1: float, b1: float, c1: float,
        a2: float, b2: float, c2: float
    ) -> Dict[str, Any]:
        """
        Resolve sistema linear 2x2 pela Regra de Cramer:
        a1*x + b1*y = c1
        a2*x + b2*y = c2
        """
        a1_v = validate_number(a1, "a1")
        b1_v = validate_number(b1, "b1")
        c1_v = validate_number(c1, "c1")
        a2_v = validate_number(a2, "a2")
        b2_v = validate_number(b2, "b2")
        c2_v = validate_number(c2, "c2")

        # Determinante principal
        det = (a1_v * b2_v) - (a2_v * b1_v)
        # Determinante de X
        det_x = (c1_v * b2_v) - (c2_v * b1_v)
        # Determinante de Y
        det_y = (a1_v * c2_v) - (a2_v * c1_v)

        passos = [
            f"Sistema informado:",
            f"  [1] ({a1_v})x + ({b1_v})y = {c1_v}",
            f"  [2] ({a2_v})x + ({b2_v})y = {c2_v}",
            f"Cálculo dos determinantes:",
            f"  D  = ({a1_v})·({b2_v}) - ({a2_v})·({b1_v}) = {det}",
            f"  Dx = ({c1_v})·({b2_v}) - ({c2_v})·({b1_v}) = {det_x}",
            f"  Dy = ({a1_v})·({c2_v}) - ({a2_v})·({c1_v}) = {det_y}",
        ]

        if det != 0:
            x = det_x / det
            y = det_y / det
            passos.append("Classificação: Sistema Possível e Determinado (SPD). Possui solução única.")
            passos.append(f"  x = Dx / D = {det_x} / {det} = {x}")
            passos.append(f"  y = Dy / D = {det_y} / {det} = {y}")
            return {
                "classificacao": "SPD",
                "descricao": "Sistema Possível e Determinado (Solução única)",
                "x": x,
                "y": y,
                "passos": passos,
            }
        else:
            if det_x == 0 and det_y == 0:
                passos.append("Classificação: Sistema Possível e Indeterminado (SPI).")
                passos.append("D = 0, Dx = 0 e Dy = 0: as retas são coincidentes, existindo infinitas soluções.")
                return {
                    "classificacao": "SPI",
                    "descricao": "Sistema Possível e Indeterminado (Infinitas soluções)",
                    "x": None,
                    "y": None,
                    "passos": passos,
                }
            else:
                passos.append("Classificação: Sistema Impossível (SI).")
                passos.append("D = 0, mas Dx ≠ 0 ou Dy ≠ 0: as retas são paralelas e distintas, portanto não há interseção.")
                return {
                    "classificacao": "SI",
                    "descricao": "Sistema Impossível (Nenhuma solução)",
                    "x": None,
                    "y": None,
                    "passos": passos,
                }

    @staticmethod
    def notable_product_square_sum(a: float, b: float) -> Dict[str, Any]:
        """(a + b)² = a² + 2ab + b²"""
        a_v = validate_number(a, "a")
        b_v = validate_number(b, "b")
        res = (a_v + b_v) ** 2
        return {
            "expressao": f"({a_v} + {b_v})²",
            "desenvolvimento": f"{a_v}² + 2·{a_v}·{b_v} + {b_v}²",
            "termos": [a_v ** 2, 2 * a_v * b_v, b_v ** 2],
            "resultado": res,
        }

    @staticmethod
    def notable_product_square_diff(a: float, b: float) -> Dict[str, Any]:
        """(a - b)² = a² - 2ab + b²"""
        a_v = validate_number(a, "a")
        b_v = validate_number(b, "b")
        res = (a_v - b_v) ** 2
        return {
            "expressao": f"({a_v} - {b_v})²",
            "desenvolvimento": f"{a_v}² - 2·{a_v}·{b_v} + {b_v}²",
            "termos": [a_v ** 2, -2 * a_v * b_v, b_v ** 2],
            "resultado": res,
        }

    @staticmethod
    def notable_product_sum_diff(a: float, b: float) -> Dict[str, Any]:
        """(a + b)(a - b) = a² - b²"""
        a_v = validate_number(a, "a")
        b_v = validate_number(b, "b")
        res = (a_v ** 2) - (b_v ** 2)
        return {
            "expressao": f"({a_v} + {b_v})·({a_v} - {b_v})",
            "desenvolvimento": f"{a_v}² - {b_v}²",
            "termos": [a_v ** 2, -(b_v ** 2)],
            "resultado": res,
        }
