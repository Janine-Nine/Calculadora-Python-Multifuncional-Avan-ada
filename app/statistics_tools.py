"""
Módulo de Estatística e Probabilidade
Implementa análise descritiva univariada, distribuições de frequência,
medidas de dispersão e cálculos de probabilidade.
"""

import math
import random
import statistics
from collections import Counter
from typing import List, Dict, Any, Union, Optional
from app.validators import validate_number, ValidationError, MathDomainError


class StatisticsEngine:
    """Motor para cálculos estatísticos e probabilísticos."""

    @staticmethod
    def parse_data_series(raw_input: Union[str, List[Union[int, float]]]) -> List[float]:
        """
        Interpreta séries de números separadas por vírgula, ponto e vírgula,
        espaço ou quebras de linha, suportando formatação brasileira.
        """
        if isinstance(raw_input, list):
            if not raw_input:
                raise ValidationError("A lista de dados fornecida está vazia.")
            return [validate_number(x, "Elemento") for x in raw_input]

        if not raw_input or not raw_input.strip():
            raise ValidationError("A série de dados informada está vazia.")

        text = raw_input.strip()
        # Normalização: substitui ponto e vírgula ou quebras de linha por espaços
        text = text.replace(';', ' ').replace('\n', ' ').replace('\t', ' ')

        # Se houver números com vírgula decimal, mas separados por espaço ou vírgula
        # Ex: "10,5 20,2" ou "10.5, 20.2"
        tokens = []
        for raw_token in text.split():
            clean = raw_token.strip(',')
            if not clean:
                continue
            # Substitui vírgula decimal por ponto
            clean = clean.replace(',', '.')
            try:
                tokens.append(float(clean))
            except ValueError as err:
                raise ValidationError(f"Valor estatístico inválido: '{raw_token}'.") from err

        if not tokens:
            raise ValidationError("Nenhum valor numérico válido foi identificado na série.")

        return tokens

    @staticmethod
    def descriptive_analysis(data: List[float]) -> Dict[str, Any]:
        """Calcula todas as estatísticas descritivas principais."""
        n = len(data)
        if n == 0:
            raise ValidationError("Conjunto de dados vazio. Insira ao menos um número.")

        sorted_data = sorted(data)
        s_min = sorted_data[0]
        s_max = sorted_data[-1]
        s_range = s_max - s_min
        s_sum = sum(sorted_data)
        mean_val = s_sum / n
        median_val = statistics.median(sorted_data)

        # Modas
        counts = Counter(sorted_data)
        max_freq = max(counts.values())
        if max_freq > 1 and len(counts) > 1 and max_freq != n:
            modes = [k for k, v in counts.items() if v == max_freq]
            modes.sort()
        else:
            modes = []  # Amodal se todos têm a mesma frequência

        # Variância e Desvio-padrão
        if n >= 2:
            var_sample = statistics.variance(sorted_data)
            stdev_sample = statistics.stdev(sorted_data)
            var_pop = statistics.pvariance(sorted_data)
            stdev_pop = statistics.pstdev(sorted_data)
        else:
            var_sample = None
            stdev_sample = None
            var_pop = 0.0
            stdev_pop = 0.0

        # Quartis
        q1 = StatisticsEngine.percentile(sorted_data, 25)
        q2 = median_val
        q3 = StatisticsEngine.percentile(sorted_data, 75)
        iqr = q3 - q1

        # Distribuição de frequências
        freq_dist = []
        for val, count in sorted(counts.items()):
            rel_freq = (count / n) * 100
            freq_dist.append({
                "valor": val,
                "frequencia_absoluta": count,
                "frequencia_relativa_pct": round(rel_freq, 2),
            })

        return {
            "n": n,
            "minimo": s_min,
            "maximo": s_max,
            "amplitude": s_range,
            "soma": s_sum,
            "media": round(mean_val, 6),
            "mediana": round(median_val, 6),
            "modas": modes,
            "amodal": len(modes) == 0,
            "variancia_amostral": round(var_sample, 6) if var_sample is not None else "Requer N >= 2",
            "desvio_padrao_amostral": round(stdev_sample, 6) if stdev_sample is not None else "Requer N >= 2",
            "variancia_populacional": round(var_pop, 6),
            "desvio_padrao_populacional": round(stdev_pop, 6),
            "q1": round(q1, 6),
            "q2": round(q2, 6),
            "q3": round(q3, 6),
            "iqr": round(iqr, 6),
            "distribuicao": freq_dist,
        }

    @staticmethod
    def weighted_mean(values: List[float], weights: List[float]) -> float:
        if len(values) != len(weights):
            raise ValidationError(
                f"Quantidade de valores ({len(values)}) difere da quantidade de pesos ({len(weights)})."
            )
        if not values:
            raise ValidationError("A lista de valores e pesos não pode estar vazia.")

        sum_weights = sum(weights)
        if sum_weights == 0:
            raise MathDomainError("A soma dos pesos não pode ser zero.")

        weighted_sum = sum(v * w for v, w in zip(values, weights))
        return weighted_sum / sum_weights

    @staticmethod
    def percentile(sorted_data: List[float], p: float) -> float:
        """Cálculo de percentil com interpolação linear padrão."""
        if not (0 <= p <= 100):
            raise ValidationError("O percentil deve estar entre 0 e 100.")
        n = len(sorted_data)
        if n == 1:
            return sorted_data[0]
        k = (p / 100.0) * (n - 1)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return sorted_data[int(k)]
        d0 = sorted_data[f] * (c - k)
        d1 = sorted_data[c] * (k - f)
        return d0 + d1

    @staticmethod
    def simple_probability(favorable: int, total: int) -> Dict[str, Any]:
        fav = validate_number(favorable, "Eventos favoráveis")
        tot = validate_number(total, "Espaço amostral (total)")
        if tot <= 0:
            raise MathDomainError("O espaço amostral total deve ser estritamente positivo.")
        if fav < 0:
            raise MathDomainError("Eventos favoráveis não podem ser negativos.")
        if fav > tot:
            raise MathDomainError("Eventos favoráveis não podem exceder o total do espaço amostral.")

        prob = fav / tot
        return {
            "favoraveis": fav,
            "total": tot,
            "probabilidade": prob,
            "probabilidade_pct": prob * 100,
            "fracao": f"{int(fav)}/{int(tot)}",
        }

    @staticmethod
    def random_number(min_val: float, max_val: float, is_integer: bool = False) -> Union[int, float]:
        mi = validate_number(min_val, "Mínimo")
        ma = validate_number(max_val, "Máximo")
        if mi > ma:
            mi, ma = ma, mi
        if is_integer:
            return random.randint(int(mi), int(ma))
        return random.uniform(mi, ma)
