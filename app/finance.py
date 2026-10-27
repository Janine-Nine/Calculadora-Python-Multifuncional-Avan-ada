"""
Módulo de Matemática Financeira
Cálculos de alta precisão com Decimal e formatação no padrão monetário brasileiro (R$ 1.250,50).
"""

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import Dict, Any, List, Union
from app.validators import ValidationError, MathDomainError


def to_decimal(val: Any, name: str = "Valor") -> Decimal:
    """Converte entradas numéricas ou strings para Decimal de forma segura."""
    if isinstance(val, Decimal):
        return val
    try:
        # Se for string com formato brasileiro (ex: 1.250,50)
        s = str(val).strip()
        if ',' in s and '.' in s:
            s = s.replace('.', '').replace(',', '.')
        elif ',' in s:
            s = s.replace(',', '.')
        return Decimal(s)
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValidationError(f"{name} inválido para valor monetário: '{val}'.") from exc


def format_brl(value: Union[Decimal, float, int]) -> str:
    """Formata um valor no padrão brasileiro: R$ 1.250,50."""
    dec = to_decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    sign = "-" if dec < 0 else ""
    abs_dec = abs(dec)
    int_part, frac_part = f"{abs_dec:.2f}".split('.')
    # Agrupa milhares com ponto
    formatted_int = ""
    for idx, char in enumerate(reversed(int_part)):
        if idx > 0 and idx % 3 == 0:
            formatted_int = '.' + formatted_int
        formatted_int = char + formatted_int
    return f"{sign}R$ {formatted_int},{frac_part}"


class FinanceEngine:
    """Motor de cálculos financeiros com Decimal."""

    @staticmethod
    def simple_interest(
        principal: Union[Decimal, float],
        rate_percent: Union[Decimal, float],
        periods: Union[Decimal, float]
    ) -> Dict[str, Any]:
        """
        Juros Simples: J = C * i * t; M = C + J.
        rate_percent: Taxa por período em porcentagem (ex: 2 para 2%).
        periods: Quantidade de períodos na mesma unidade da taxa.
        """
        c = to_decimal(principal, "Capital inicial")
        i = to_decimal(rate_percent, "Taxa de juros") / Decimal("100")
        t = to_decimal(periods, "Prazo/Período")

        if c < 0 or t < 0:
            raise MathDomainError("Capital e prazo não podem ser negativos.")

        juros = (c * i * t).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        montante = (c + juros).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return {
            "capital": c,
            "taxa_pct": rate_percent,
            "periodos": t,
            "juros": juros,
            "montante": montante,
            "capital_fmt": format_brl(c),
            "juros_fmt": format_brl(juros),
            "montante_fmt": format_brl(montante),
        }

    @staticmethod
    def compound_interest(
        principal: Union[Decimal, float],
        rate_percent: Union[Decimal, float],
        periods: int
    ) -> Dict[str, Any]:
        """
        Juros Compostos: M = C * (1 + i)^t; J = M - C.
        """
        c = to_decimal(principal, "Capital inicial")
        i = to_decimal(rate_percent, "Taxa de juros") / Decimal("100")
        t = int(to_decimal(periods, "Prazo"))

        if c < 0 or t < 0:
            raise MathDomainError("Capital e prazo não podem ser negativos.")

        factor = (Decimal("1") + i) ** t
        montante = (c * factor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        juros = (montante - c).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return {
            "capital": c,
            "taxa_pct": rate_percent,
            "periodos": t,
            "juros": juros,
            "montante": montante,
            "capital_fmt": format_brl(c),
            "juros_fmt": format_brl(juros),
            "montante_fmt": format_brl(montante),
        }

    @staticmethod
    def convert_interest_rate(rate_percent: float, from_type: str, to_type: str) -> Dict[str, Any]:
        """
        Converte taxas equivalentes: 'mensal' <-> 'anual'.
        i_anual = (1 + i_mensal)^12 - 1
        i_mensal = (1 + i_anual)^(1/12) - 1
        """
        r = float(rate_percent) / 100.0
        from_t = from_type.lower()
        to_t = to_type.lower()

        if from_t == to_t:
            return {"taxa_convertida": rate_percent, "formula": "Mesma periodicidade"}

        if from_t == "mensal" and to_t == "anual":
            converted = ((1.0 + r) ** 12 - 1.0) * 100.0
            return {
                "origem": "Mensal",
                "destino": "Anual",
                "taxa_original_pct": rate_percent,
                "taxa_convertida_pct": round(converted, 4),
                "formula": "i_anual = (1 + i_mensal)^12 - 1",
            }
        elif from_t == "anual" and to_t == "mensal":
            converted = ((1.0 + r) ** (1.0 / 12.0) - 1.0) * 100.0
            return {
                "origem": "Anual",
                "destino": "Mensal",
                "taxa_original_pct": rate_percent,
                "taxa_convertida_pct": round(converted, 4),
                "formula": "i_mensal = (1 + i_anual)^(1/12) - 1",
            }
        else:
            raise ValidationError("Conversão suportada apenas entre 'mensal' e 'anual'.")

    @staticmethod
    def price_table_financing(
        loan_amount: Union[Decimal, float],
        monthly_rate_percent: Union[Decimal, float],
        installments_count: int
    ) -> Dict[str, Any]:
        """
        Sistema Francês de Amortização (Tabela Price) - Prestações Fixas:
        PMT = PV * [i * (1 + i)^n] / [(1 + i)^n - 1]
        """
        pv = to_decimal(loan_amount, "Valor financiado")
        i = (to_decimal(monthly_rate_percent, "Taxa mensal") / Decimal("100"))
        n = int(to_decimal(installments_count, "Número de parcelas"))

        if pv <= 0 or n <= 0:
            raise MathDomainError("Valor financiado e número de parcelas devem ser positivos.")

        if i == 0:
            pmt = (pv / Decimal(n)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            total_paid = pv
            total_interest = Decimal("0.00")
        else:
            # Fórmula Price
            factor = (Decimal("1") + i) ** n
            pmt = (pv * (i * factor) / (factor - Decimal("1"))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            total_paid = (pmt * n).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            total_interest = (total_paid - pv).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return {
            "valor_financiado": pv,
            "taxa_mensal_pct": monthly_rate_percent,
            "parcelas_total": n,
            "valor_parcela": pmt,
            "total_pago": total_paid,
            "total_juros": total_interest,
            "valor_parcela_fmt": format_brl(pmt),
            "total_pago_fmt": format_brl(total_paid),
            "total_juros_fmt": format_brl(total_interest),
        }

    @staticmethod
    def margin_and_markup(cost: Union[Decimal, float], sale_price: Union[Decimal, float]) -> Dict[str, Any]:
        """
        Calcula Lucro Bruto, Margem de Lucro e Markup:
        Lucro = PV - Custo
        Margem = (Lucro / PV) * 100
        Markup = (Lucro / Custo) * 100
        """
        c = to_decimal(cost, "Custo")
        pv = to_decimal(sale_price, "Preço de Venda")

        if c <= 0 or pv <= 0:
            raise MathDomainError("Custo e preço de venda devem ser maiores que zero.")

        lucro = pv - c
        margem_pct = ((lucro / pv) * Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        markup_pct = ((lucro / c) * Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return {
            "custo": c,
            "preco_venda": pv,
            "lucro_bruto": lucro,
            "margem_lucro_pct": margem_pct,
            "markup_pct": markup_pct,
            "custo_fmt": format_brl(c),
            "preco_venda_fmt": format_brl(pv),
            "lucro_bruto_fmt": format_brl(lucro),
        }

    @staticmethod
    def price_from_desired_margin(cost: Union[Decimal, float], desired_margin_pct: Union[Decimal, float]) -> Dict[str, Any]:
        """Preço de Venda = Custo / (1 - Margem/100)"""
        c = to_decimal(cost, "Custo")
        m = to_decimal(desired_margin_pct, "Margem desejada")
        if m >= 100:
            raise MathDomainError("Margem de lucro desejada não pode ser igual ou superior a 100%.")
        sale_price = (c / (Decimal("1") - (m / Decimal("100")))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return {
            "custo": c,
            "margem_desejada_pct": m,
            "preco_sugerido": sale_price,
            "preco_sugerido_fmt": format_brl(sale_price),
        }

    @staticmethod
    def price_from_desired_markup(cost: Union[Decimal, float], desired_markup_pct: Union[Decimal, float]) -> Dict[str, Any]:
        """Preço de Venda = Custo * (1 + Markup/100)"""
        c = to_decimal(cost, "Custo")
        mk = to_decimal(desired_markup_pct, "Markup desejado")
        sale_price = (c * (Decimal("1") + (mk / Decimal("100")))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return {
            "custo": c,
            "markup_desejado_pct": mk,
            "preco_sugerido": sale_price,
            "preco_sugerido_fmt": format_brl(sale_price),
        }

    @staticmethod
    def investment_with_monthly_contributions(
        initial_amount: Union[Decimal, float],
        monthly_deposit: Union[Decimal, float],
        monthly_rate_percent: Union[Decimal, float],
        months: int
    ) -> Dict[str, Any]:
        """
        Simulação de Investimentos com Aportes Mensais:
        FV = C*(1+i)^n + PMT*[((1+i)^n - 1) / i]
        """
        c = to_decimal(initial_amount, "Aporte inicial")
        pmt = to_decimal(monthly_deposit, "Aporte mensal")
        i = to_decimal(monthly_rate_percent, "Taxa mensal") / Decimal("100")
        n = int(to_decimal(months, "Meses"))

        if c < 0 or pmt < 0 or n <= 0:
            raise MathDomainError("Valores devem ser não-negativos e meses > 0.")

        total_invested = c + (pmt * n)

        if i == 0:
            final_balance = total_invested
        else:
            factor = (Decimal("1") + i) ** n
            fv_initial = c * factor
            fv_deposits = pmt * ((factor - Decimal("1")) / i)
            final_balance = (fv_initial + fv_deposits).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        interest_earned = (final_balance - total_invested).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return {
            "total_investido": total_invested,
            "saldo_final": final_balance,
            "juros_acumulados": interest_earned,
            "meses": n,
            "total_investido_fmt": format_brl(total_invested),
            "saldo_final_fmt": format_brl(final_balance),
            "juros_acumulados_fmt": format_brl(interest_earned),
        }

    @staticmethod
    def inflation_loss(amount: Union[Decimal, float], annual_inflation_pct: Union[Decimal, float], years: int) -> Dict[str, Any]:
        """
        Simula o poder de compra futuro considerando inflação:
        Poder_Compra = Valor / (1 + inflação)^anos
        """
        val = to_decimal(amount, "Valor nominal")
        inf = to_decimal(annual_inflation_pct, "Inflação anual") / Decimal("100")
        y = int(to_decimal(years, "Anos"))

        future_purchasing_power = (val / ((Decimal("1") + inf) ** y)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        loss = (val - future_purchasing_power).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return {
            "valor_nominal": val,
            "poder_compra_futuro": future_purchasing_power,
            "perda_poder_compra": loss,
            "anos": y,
            "valor_nominal_fmt": format_brl(val),
            "poder_compra_futuro_fmt": format_brl(future_purchasing_power),
            "perda_poder_compra_fmt": format_brl(loss),
        }
