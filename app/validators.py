"""
Módulo de Validação e Segurança
Contém validações de domínio matemático, limites operacionais e verificação de integridade.
"""

import math
from typing import Any, List, Union


class ValidationError(Exception):
    """Exceção levantada quando uma validação de negócio ou matemática falha."""
    pass


class MathDomainError(ValidationError):
    """Exceção para entradas fora do domínio permitido para a operação."""
    pass


def validate_number(value: Any, name: str = "Valor") -> float:
    """Valida se uma entrada pode ser convertida com segurança para float."""
    try:
        val = float(value)
        if math.isnan(val) or math.isinf(val):
            raise MathDomainError(f"{name} não pode ser infinito ou NaN.")
        return val
    except (ValueError, TypeError) as exc:
        raise ValidationError(f"{name} inválido: '{value}'. Informe um número válido.") from exc


def validate_non_zero(value: Union[int, float], name: str = "Divisor") -> float:
    """Garante que um divisor não seja zero."""
    val = validate_number(value, name)
    if val == 0:
        raise MathDomainError(f"Divisão por zero não é permitida para {name}.")
    return val


def validate_non_negative(value: Union[int, float], name: str = "Valor") -> float:
    """Garante que o valor seja maior ou igual a zero."""
    val = validate_number(value, name)
    if val < 0:
        raise MathDomainError(f"{name} deve ser não-negativo (>= 0). Recebido: {val}.")
    return val


def validate_positive(value: Union[int, float], name: str = "Valor") -> float:
    """Garante que o valor seja estritamente positivo (> 0)."""
    val = validate_number(value, name)
    if val <= 0:
        raise MathDomainError(f"{name} deve ser estritamente positivo (> 0). Recebido: {val}.")
    return val


def validate_integer(value: Any, name: str = "Valor") -> int:
    """Valida se o valor é um número inteiro válido."""
    try:
        val = float(value)
        if not val.is_integer():
            raise ValidationError(f"{name} deve ser um número inteiro. Recebido: {value}.")
        return int(val)
    except (ValueError, TypeError) as exc:
        raise ValidationError(f"{name} inválido para inteiro: '{value}'.") from exc


def validate_non_negative_integer(value: Any, name: str = "Valor", max_limit: int = 1000) -> int:
    """Valida inteiro não-negativo com teto de segurança contra estouro de CPU."""
    val = validate_integer(value, name)
    if val < 0:
        raise MathDomainError(f"{name} não pode ser negativo. Recebido: {val}.")
    if val > max_limit:
        raise MathDomainError(f"{name} excede o limite máximo suportado de {max_limit} para segurança.")
    return val


def validate_matrix_dimensions(matrix: List[List[float]], name: str = "Matriz") -> tuple[int, int]:
    """Valida se uma matriz é regular (todas as linhas têm o mesmo tamanho) e não-vazia."""
    if not matrix or not isinstance(matrix, list):
        raise ValidationError(f"{name} está vazia ou não é uma lista de listas.")
    rows = len(matrix)
    cols = len(matrix[0])
    if cols == 0:
        raise ValidationError(f"{name} possui linhas vazias.")
    for i, row in enumerate(matrix):
        if not isinstance(row, list) or len(row) != cols:
            raise ValidationError(f"Linha {i+1} de {name} tem dimensão incompatível. Esperado: {cols} colunas.")
    return rows, cols
