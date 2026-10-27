"""
Módulo de Geometria Plana e Espacial
Cálculo de áreas, perímetros, volumes, áreas superficiais,
Teorema de Pitágoras e distância euclidiana entre pontos.
"""

import math
from typing import Dict, Any, Tuple
from app.validators import validate_positive, validate_number, MathDomainError


class GeometryCalculator:
    """Calculadora de geometria 2D e 3D com fórmulas e validações estritas."""

    # --- GEOMETRIA PLANA (2D) ---

    @staticmethod
    def square(side: float) -> Dict[str, Any]:
        s = validate_positive(side, "Lado do quadrado")
        area = s ** 2
        perim = 4 * s
        return {
            "figura": "Quadrado",
            "lado": s,
            "area": area,
            "perimetro": perim,
            "formula_area": "A = L²",
            "formula_perimetro": "P = 4L",
        }

    @staticmethod
    def rectangle(width: float, height: float) -> Dict[str, Any]:
        w = validate_positive(width, "Largura")
        h = validate_positive(height, "Altura")
        area = w * h
        perim = 2 * (w + h)
        return {
            "figura": "Retângulo",
            "largura": w,
            "altura": h,
            "area": area,
            "perimetro": perim,
            "formula_area": "A = base × altura",
            "formula_perimetro": "P = 2 × (base + altura)",
        }

    @staticmethod
    def triangle(base: float, height: float, side_a: float = 0.0, side_b: float = 0.0) -> Dict[str, Any]:
        b = validate_positive(base, "Base do triângulo")
        h = validate_positive(height, "Altura do triângulo")
        area = (b * h) / 2.0
        perim = (b + side_a + side_b) if (side_a > 0 and side_b > 0) else None
        return {
            "figura": "Triângulo",
            "base": b,
            "altura": h,
            "area": area,
            "perimetro": perim,
            "formula_area": "A = (b × h) / 2",
        }

    @staticmethod
    def circle(radius: float) -> Dict[str, Any]:
        r = validate_positive(radius, "Raio do círculo")
        area = math.pi * (r ** 2)
        circumference = 2 * math.pi * r
        return {
            "figura": "Círculo",
            "raio": r,
            "diametro": 2 * r,
            "area": area,
            "circunferencia": circumference,
            "formula_area": "A = π × r²",
            "formula_circunferencia": "C = 2 × π × r",
        }

    @staticmethod
    def parallelogram(base: float, height: float, side: float = 0.0) -> Dict[str, Any]:
        b = validate_positive(base, "Base")
        h = validate_positive(height, "Altura")
        area = b * h
        perim = 2 * (b + side) if side > 0 else None
        return {
            "figura": "Paralelogramo",
            "base": b,
            "altura": h,
            "area": area,
            "perimetro": perim,
            "formula_area": "A = base × altura",
        }

    @staticmethod
    def trapezoid(big_base: float, small_base: float, height: float) -> Dict[str, Any]:
        b_big = validate_positive(big_base, "Base maior (B)")
        b_sml = validate_positive(small_base, "Base menor (b)")
        h = validate_positive(height, "Altura (h)")
        area = ((b_big + b_sml) * h) / 2.0
        return {
            "figura": "Trapézio",
            "base_maior": b_big,
            "base_menor": b_sml,
            "altura": h,
            "area": area,
            "formula_area": "A = ((B + b) × h) / 2",
        }

    # --- GEOMETRIA ESPACIAL (3D) ---

    @staticmethod
    def cube(edge: float) -> Dict[str, Any]:
        a = validate_positive(edge, "Aresta do cubo")
        volume = a ** 3
        surface_area = 6 * (a ** 2)
        return {
            "solido": "Cubo",
            "aresta": a,
            "volume": volume,
            "area_superficial": surface_area,
            "formula_volume": "V = a³",
            "formula_area": "A = 6 × a²",
        }

    @staticmethod
    def rectangular_prism(a: float, b: float, c: float) -> Dict[str, Any]:
        a_v = validate_positive(a, "Comprimento")
        b_v = validate_positive(b, "Largura")
        c_v = validate_positive(c, "Altura")
        volume = a_v * b_v * c_v
        surface_area = 2 * (a_v * b_v + b_v * c_v + a_v * c_v)
        return {
            "solido": "Paralelepípedo",
            "comprimento": a_v,
            "largura": b_v,
            "altura": c_v,
            "volume": volume,
            "area_superficial": surface_area,
            "formula_volume": "V = a × b × c",
            "formula_area": "A = 2 × (ab + bc + ac)",
        }

    @staticmethod
    def cylinder(radius: float, height: float) -> Dict[str, Any]:
        r = validate_positive(radius, "Raio do cilindro")
        h = validate_positive(height, "Altura do cilindro")
        volume = math.pi * (r ** 2) * h
        surface_area = 2 * math.pi * r * (r + h)
        return {
            "solido": "Cilindro",
            "raio": r,
            "altura": h,
            "volume": volume,
            "area_superficial": surface_area,
            "formula_volume": "V = π × r² × h",
            "formula_area": "A = 2πr(r + h)",
        }

    @staticmethod
    def cone(radius: float, height: float) -> Dict[str, Any]:
        r = validate_positive(radius, "Raio do cone")
        h = validate_positive(height, "Altura do cone")
        slant = math.sqrt(r ** 2 + h ** 2)  # geratriz
        volume = (1.0 / 3.0) * math.pi * (r ** 2) * h
        surface_area = math.pi * r * (r + slant)
        return {
            "solido": "Cone",
            "raio": r,
            "altura": h,
            "geratriz": slant,
            "volume": volume,
            "area_superficial": surface_area,
            "formula_volume": "V = (1/3) × π × r² × h",
            "formula_area": "A = π × r × (r + g)",
        }

    @staticmethod
    def sphere(radius: float) -> Dict[str, Any]:
        r = validate_positive(radius, "Raio da esfera")
        volume = (4.0 / 3.0) * math.pi * (r ** 3)
        surface_area = 4 * math.pi * (r ** 2)
        return {
            "solido": "Esfera",
            "raio": r,
            "volume": volume,
            "area_superficial": surface_area,
            "formula_volume": "V = (4/3) × π × r³",
            "formula_area": "A = 4 × π × r²",
        }

    # --- PITÁGORAS E DISTÂNCIA ---

    @staticmethod
    def pythagoras_hypotenuse(cathetus_a: float, cathetus_b: float) -> Dict[str, Any]:
        a = validate_positive(cathetus_a, "Cateto a")
        b = validate_positive(cathetus_b, "Cateto b")
        c = math.sqrt(a ** 2 + b ** 2)
        return {
            "teorema": "Pitágoras (Hipotenusa)",
            "cateto_a": a,
            "cateto_b": b,
            "hipotenusa": c,
            "formula": "c = √(a² + b²)",
            "passos": f"c = √({a}² + {b}²) = √({a**2} + {b**2}) = √{a**2 + b**2} = {c:.4f}",
        }

    @staticmethod
    def pythagoras_cathetus(hypotenuse: float, known_cathetus: float) -> Dict[str, Any]:
        c = validate_positive(hypotenuse, "Hipotenusa (c)")
        b = validate_positive(known_cathetus, "Cateto conhecido (b)")
        if b >= c:
            raise MathDomainError("Em um triângulo retângulo, o cateto deve ser estritamente menor que a hipotenusa.")
        a = math.sqrt(c ** 2 - b ** 2)
        return {
            "teorema": "Pitágoras (Cateto desconhecido)",
            "hipotenusa": c,
            "cateto_conhecido": b,
            "cateto_calculado": a,
            "formula": "a = √(c² - b²)",
            "passos": f"a = √({c}² - {b}²) = √({c**2} - {b**2}) = √{c**2 - b**2} = {a:.4f}",
        }

    @staticmethod
    def distance_2d(x1: float, y1: float, x2: float, y2: float) -> Dict[str, Any]:
        p1_x = validate_number(x1, "x1")
        p1_y = validate_number(y1, "y1")
        p2_x = validate_number(x2, "x2")
        p2_y = validate_number(y2, "y2")
        dx = p2_x - p1_x
        dy = p2_y - p1_y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        return {
            "ponto_1": (p1_x, p1_y),
            "ponto_2": (p2_x, p2_y),
            "distancia": dist,
            "formula": "d = √((x₂ - x₁)² + (y₂ - y₁)²)",
            "passos": f"d = √(({p2_x} - {p1_x})² + ({p2_y} - {p1_y})²) = √({dx**2} + {dy**2}) = {dist:.4f}",
        }
