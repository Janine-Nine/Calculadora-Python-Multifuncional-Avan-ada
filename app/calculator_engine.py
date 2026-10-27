"""
Motor Central da Calculadora (Calculator Engine)
Gerencia o estado da calculadora básica e científica, memória, histórico
e avaliação segura de expressões.
"""

from typing import Union, Optional, Tuple, Dict, Any
from app.expression_parser import SafeExpressionParser
from app.history import HistoryManager
from app.settings import SettingsManager
from app.validators import ValidationError, MathDomainError


class CalculatorEngine:
    """Motor unificado de cálculo para operações básicas, científicas e memória."""

    def __init__(
        self,
        history_mgr: Optional[HistoryManager] = None,
        settings_mgr: Optional[SettingsManager] = None
    ):
        self.history = history_mgr or HistoryManager()
        self.settings = settings_mgr or SettingsManager()
        self.memory: float = 0.0
        self.has_memory: bool = False
        self.last_expression: str = ""
        self.last_result: str = ""

    @property
    def angle_mode(self) -> str:
        return self.settings.get("angle_mode", "deg")

    def set_angle_mode(self, mode: str) -> None:
        if mode.lower() in ("deg", "rad"):
            self.settings.set("angle_mode", mode.lower())

    def evaluate_expression(self, expression: str, category: str = "Básica") -> Tuple[str, Optional[float]]:
        """
        Executa a expressão com o parser seguro, formata o resultado
        e salva no histórico persistente.
        """
        if not expression or not expression.strip():
            raise ValidationError("Expressão em branco.")

        parser = SafeExpressionParser(angle_mode=self.angle_mode)
        raw_result = parser.evaluate(expression)

        # Formatação de acordo com a precisão
        prec = self.settings.get("precision", 6)
        if isinstance(raw_result, float):
            formatted_res = f"{round(raw_result, prec):.{prec}g}"
        else:
            formatted_res = str(raw_result)

        # Substitui ponto por vírgula se configurado separador decimal brasileiro
        sep = self.settings.get("decimal_separator", ",")
        if sep == ",":
            # Formata número para exibição mantendo padrão BR
            display_res = formatted_res.replace('.', ',')
        else:
            display_res = formatted_res

        self.last_expression = expression
        self.last_result = display_res

        # Adiciona ao histórico persistente
        self.history.add_entry(expression, display_res, category=category)

        return display_res, float(raw_result)

    # --- OPERAÇÕES RÁPIDAS DE MEMÓRIA ---

    def memory_clear(self) -> None:
        self.memory = 0.0
        self.has_memory = False

    def memory_recall(self) -> float:
        return self.memory

    def memory_add(self, value: float) -> float:
        self.memory += float(value)
        self.has_memory = True
        return self.memory

    def memory_subtract(self, value: float) -> float:
        self.memory -= float(value)
        self.has_memory = True
        return self.memory

    def memory_store(self, value: float) -> float:
        self.memory = float(value)
        self.has_memory = True
        return self.memory

    # --- OPERAÇÕES DIRETAS NO DISPLAY ---

    @staticmethod
    def toggle_sign(current_val: str) -> str:
        s = current_val.strip()
        if not s or s == "0":
            return "0"
        if s.startswith("-"):
            return s[1:]
        return "-" + s

    @staticmethod
    def inverse(value: float) -> float:
        if value == 0:
            raise MathDomainError("Divisão por zero: não existe inverso multiplicativo de 0.")
        return 1.0 / value

    @staticmethod
    def percentage(value: float, base: Optional[float] = None) -> float:
        """Se houver base, calcula x% da base. Caso contrário, divide por 100."""
        if base is not None:
            return (base * value) / 100.0
        return value / 100.0
