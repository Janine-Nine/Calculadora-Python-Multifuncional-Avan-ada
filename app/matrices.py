"""
Módulo de Matrizes e Vetores
Operações lineares fundamentais: soma, subtração, multiplicação matricial e escalar,
transposição, determinante e álgebra vetorial (produto escalar e norma).
"""

import math
from typing import List, Union
from app.validators import validate_matrix_dimensions, validate_number, ValidationError, MathDomainError

Matrix = List[List[float]]
Vector = List[float]


class MatrixEngine:
    """Motor de cálculo vetorial e matricial com validação rigorosa de dimensões."""

    @staticmethod
    def add(a: Matrix, b: Matrix) -> Matrix:
        r1, c1 = validate_matrix_dimensions(a, "Matriz A")
        r2, c2 = validate_matrix_dimensions(b, "Matriz B")
        if r1 != r2 or c1 != c2:
            raise ValidationError(
                f"Dimensões incompatíveis para soma: A tem {r1}x{c1} e B tem {r2}x{c2}. "
                f"Ambas devem ter exatamente as mesmas dimensões."
            )
        return [[a[i][j] + b[i][j] for j in range(c1)] for i in range(r1)]

    @staticmethod
    def subtract(a: Matrix, b: Matrix) -> Matrix:
        r1, c1 = validate_matrix_dimensions(a, "Matriz A")
        r2, c2 = validate_matrix_dimensions(b, "Matriz B")
        if r1 != r2 or c1 != c2:
            raise ValidationError(
                f"Dimensões incompatíveis para subtração: A tem {r1}x{c1} e B tem {r2}x{c2}."
            )
        return [[a[i][j] - b[i][j] for j in range(c1)] for i in range(r1)]

    @staticmethod
    def multiply_scalar(a: Matrix, scalar: float) -> Matrix:
        r, c = validate_matrix_dimensions(a, "Matriz A")
        s = validate_number(scalar, "Escalar")
        return [[a[i][j] * s for j in range(c)] for i in range(r)]

    @staticmethod
    def multiply(a: Matrix, b: Matrix) -> Matrix:
        r1, c1 = validate_matrix_dimensions(a, "Matriz A")
        r2, c2 = validate_matrix_dimensions(b, "Matriz B")
        if c1 != r2:
            raise ValidationError(
                f"Dimensões incompatíveis para multiplicação matricial: "
                f"Colunas de A ({c1}) devem ser iguais às Linhas de B ({r2})."
            )
        result = [[0.0 for _ in range(c2)] for _ in range(r1)]
        for i in range(r1):
            for j in range(c2):
                result[i][j] = sum(a[i][k] * b[k][j] for k in range(c1))
        return result

    @staticmethod
    def transpose(a: Matrix) -> Matrix:
        r, c = validate_matrix_dimensions(a, "Matriz A")
        return [[a[i][j] for i in range(r)] for j in range(c)]

    @staticmethod
    def determinant(a: Matrix) -> float:
        r, c = validate_matrix_dimensions(a, "Matriz A")
        if r != c:
            raise ValidationError(f"O determinante só é definido para matrizes quadradas. Matriz informada é {r}x{c}.")

        n = r
        if n == 1:
            return float(a[0][0])
        elif n == 2:
            return float((a[0][0] * a[1][1]) - (a[0][1] * a[1][0]))
        elif n == 3:
            # Regra de Sarrus
            pos = (
                a[0][0] * a[1][1] * a[2][2]
                + a[0][1] * a[1][2] * a[2][0]
                + a[0][2] * a[1][0] * a[2][1]
            )
            neg = (
                a[0][2] * a[1][1] * a[2][0]
                + a[0][0] * a[1][2] * a[2][1]
                + a[0][1] * a[1][0] * a[2][2]
            )
            return float(pos - neg)
        else:
            # Eliminação Gaussiana com pivoteamento para matrizes maiores
            mat = [row[:] for row in a]
            det = 1.0
            for i in range(n):
                pivot = i
                for k in range(i + 1, n):
                    if abs(mat[k][i]) > abs(mat[pivot][i]):
                        pivot = k
                if abs(mat[pivot][i]) < 1e-12:
                    return 0.0
                if pivot != i:
                    mat[i], mat[pivot] = mat[pivot], mat[i]
                    det = -det
                det *= mat[i][i]
                for k in range(i + 1, n):
                    factor = mat[k][i] / mat[i][i]
                    for j in range(i, n):
                        mat[k][j] -= factor * mat[i][j]
            return float(det)

    # --- VETORES ---

    @staticmethod
    def vector_dot_product(u: Vector, v: Vector) -> float:
        if not u or not v:
            raise ValidationError("Vetores não podem estar vazios.")
        if len(u) != len(v):
            raise ValidationError(
                f"Vetores com dimensões distintas para produto escalar ({len(u)} != {len(v)})."
            )
        return sum(u[i] * v[i] for i in range(len(u)))

    @staticmethod
    def vector_norm(u: Vector) -> float:
        if not u:
            raise ValidationError("Vetor vazio para cálculo de norma.")
        return math.sqrt(sum(x ** 2 for x in u))
