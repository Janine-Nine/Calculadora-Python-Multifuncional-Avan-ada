"""
Módulo de Cálculos de Data e Hora
Diferença entre datas, contagem de dias úteis, cálculo de idade,
operações com intervalos de tempo e validação de calendário gregoriano.
"""

from datetime import date, datetime, timedelta
from typing import Dict, Any, Union
from app.validators import ValidationError, MathDomainError


DIAS_SEMANA_PT = [
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
    "Sábado",
    "Domingo",
]


class DateTimeCalculator:
    """Calculadora de datas, horários e dias úteis."""

    @staticmethod
    def parse_date(date_str: str) -> date:
        """Aceita formatos 'DD/MM/AAAA' ou 'AAAA-MM-DD'."""
        if not date_str or not date_str.strip():
            raise ValidationError("Data vazia. Informe uma data válida.")

        clean = date_str.strip()
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
            try:
                return datetime.strptime(clean, fmt).date()
            except ValueError:
                pass
        raise ValidationError(f"Formato de data inválido: '{date_str}'. Utilize DD/MM/AAAA ou AAAA-MM-DD.")

    @staticmethod
    def date_difference(d1_str: str, d2_str: str) -> Dict[str, Any]:
        """Calcula a diferença entre duas datas em dias, semanas e anos/meses/dias aproximados."""
        d1 = DateTimeCalculator.parse_date(d1_str)
        d2 = DateTimeCalculator.parse_date(d2_str)

        start = min(d1, d2)
        end = max(d1, d2)

        total_days = (end - start).days
        total_weeks = total_days // 7
        remainder_days = total_days % 7

        # Decomposição em anos, meses e dias
        years = end.year - start.year
        months = end.month - start.month
        days = end.day - start.day

        if days < 0:
            months -= 1
            # Dias do mês anterior ao mês de 'end'
            prev_month = end.month - 1 if end.month > 1 else 12
            prev_year = end.year if end.month > 1 else end.year - 1
            # Cálculo de dias no mês anterior
            d_prev = (date(end.year, end.month, 1) - timedelta(days=1)).day
            days += d_prev

        if months < 0:
            years -= 1
            months += 12

        business_days = DateTimeCalculator.count_business_days(start, end)

        return {
            "data_inicial": start.strftime("%d/%m/%Y"),
            "data_final": end.strftime("%d/%m/%Y"),
            "total_dias": total_days,
            "total_semanas": total_weeks,
            "dias_restantes": remainder_days,
            "dias_uteis": business_days,
            "anos": years,
            "meses": months,
            "dias": days,
            "resumo": f"{years} anos, {months} meses e {days} dias ({total_days} dias no total)",
        }

    @staticmethod
    def calculate_age(birth_date_str: str, reference_date_str: str = "") -> Dict[str, Any]:
        """Calcula idade a partir da data de nascimento."""
        birth = DateTimeCalculator.parse_date(birth_date_str)
        ref = DateTimeCalculator.parse_date(reference_date_str) if reference_date_str else date.today()

        if birth > ref:
            raise MathDomainError("A data de nascimento não pode ser posterior à data de referência.")

        diff = DateTimeCalculator.date_difference(birth.strftime("%d/%m/%Y"), ref.strftime("%d/%m/%Y"))
        return {
            "nascimento": birth.strftime("%d/%m/%Y"),
            "referencia": ref.strftime("%d/%m/%Y"),
            "idade_anos": diff["anos"],
            "idade_meses": diff["meses"],
            "idade_dias": diff["dias"],
            "total_dias_vida": diff["total_dias"],
            "resumo": f"{diff['anos']} anos, {diff['meses']} meses e {diff['dias']} dias de vida.",
        }

    @staticmethod
    def count_business_days(start_date: Union[date, str], end_date: Union[date, str]) -> int:
        """Conta dias úteis (segunda a sexta) entre duas datas inclusive o início e fim."""
        d1 = start_date if isinstance(start_date, date) else DateTimeCalculator.parse_date(start_date)
        d2 = end_date if isinstance(end_date, date) else DateTimeCalculator.parse_date(end_date)

        start = min(d1, d2)
        end = max(d1, d2)

        cur = start
        business_days = 0
        while cur <= end:
            # 0=Segunda, ..., 4=Sexta, 5=Sábado, 6=Domingo
            if cur.weekday() < 5:
                business_days += 1
            cur += timedelta(days=1)
        return business_days

    @staticmethod
    def add_or_subtract_days(base_date_str: str, days_count: int) -> Dict[str, Any]:
        base = DateTimeCalculator.parse_date(base_date_str)
        result_date = base + timedelta(days=days_count)
        weekday_name = DIAS_SEMANA_PT[result_date.weekday()]
        return {
            "data_base": base.strftime("%d/%m/%Y"),
            "dias_ajustados": days_count,
            "data_resultante": result_date.strftime("%d/%m/%Y"),
            "dia_da_semana": weekday_name,
            "ano_bissexto": DateTimeCalculator.is_leap_year(result_date.year),
        }

    @staticmethod
    def is_leap_year(year: int) -> bool:
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    @staticmethod
    def get_weekday(date_str: str) -> str:
        d = DateTimeCalculator.parse_date(date_str)
        return DIAS_SEMANA_PT[d.weekday()]

    @staticmethod
    def convert_time_units(seconds: float) -> Dict[str, Any]:
        """Converte segundos em horas, minutos e segundos decompostos."""
        if seconds < 0:
            raise MathDomainError("Segundos não podem ser negativos.")
        total_sec = int(seconds)
        hours = total_sec // 3600
        rem = total_sec % 3600
        minutes = rem // 60
        secs = rem % 60
        return {
            "total_segundos": seconds,
            "horas": hours,
            "minutos": minutes,
            "segundos": secs,
            "formatado": f"{hours:02d}:{minutes:02d}:{secs:02d}",
        }
