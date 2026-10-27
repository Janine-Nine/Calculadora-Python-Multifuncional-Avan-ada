"""
Interface Gráfica Desktop (Tkinter / ttk) - Python Ultimate Calculator
Visual moderno, paleta escura (preto, grafite, violeta), navegação em abas,
atalhos de teclado, integração com matplotlib e suporte a todas as categorias.
"""

import math
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from app.calculator_engine import CalculatorEngine
from app.scientific import ScientificCalculator
from app.fractions_math import FractionsMath
from app.algebra import AlgebraSolver
from app.statistics_tools import StatisticsEngine
from app.finance import FinanceEngine, format_brl
from app.converters import UnitConverter
from app.date_time import DateTimeCalculator
from app.geometry import GeometryCalculator
from app.matrices import MatrixEngine
from app.history import HistoryManager
from app.settings import SettingsManager
from app.validators import ValidationError, MathDomainError


# Paleta de Cores (Tema Escuro Tecnológico)
COLORS = {
    "bg_dark": "#0a0b10",
    "surface": "#13141f",
    "surface_alt": "#1c1e2e",
    "border": "#2d314a",
    "accent_primary": "#7c3aed",      # Roxo principal
    "accent_hover": "#6d28d9",
    "accent_light": "#a855f7",        # Violeta luminoso
    "text_primary": "#f8fafc",
    "text_muted": "#94a3b8",
    "btn_num_bg": "#1e2238",
    "btn_num_fg": "#ffffff",
    "btn_op_bg": "#2a2147",
    "btn_op_fg": "#c084fc",
    "btn_fn_bg": "#161b30",
    "btn_fn_fg": "#93c5fd",
    "btn_equal_bg": "#7c3aed",
    "btn_equal_fg": "#ffffff",
    "danger": "#ef4444",
    "success": "#10b981",
}


class UltimateCalculatorGUI:
    """Janela principal da calculadora com abas temáticas e atalhos de teclado."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Python Ultimate Calculator — Calculadora Multifuncional Avançada")
        self.root.geometry("1080x750")
        self.root.minsize(860, 640)
        self.root.configure(bg=COLORS["bg_dark"])

        # Motores de Lógica
        self.history_mgr = HistoryManager()
        self.settings_mgr = SettingsManager()
        self.engine = CalculatorEngine(self.history_mgr, self.settings_mgr)

        # Variáveis de Estado da Calculadora Básica/Científica
        self.current_expr = tk.StringVar(value="")
        self.display_result = tk.StringVar(value="0")
        self.angle_mode_var = tk.StringVar(value=self.engine.angle_mode.upper())

        self._configure_styles()
        self._build_main_layout()
        self._bind_keyboard_shortcuts()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Notebook (Abas)
        style.configure("TNotebook", background=COLORS["bg_dark"], borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background=COLORS["surface"],
            foreground=COLORS["text_muted"],
            padding=[14, 8],
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", COLORS["accent_primary"])],
            foreground=[("selected", "#ffffff")],
        )

        style.configure("TFrame", background=COLORS["surface"])
        style.configure("TLabelframe", background=COLORS["surface"], foreground=COLORS["accent_light"])
        style.configure("TLabelframe.Label", background=COLORS["surface"], foreground=COLORS["accent_light"], font=("Segoe UI", 10, "bold"))
        style.configure("TLabel", background=COLORS["surface"], foreground=COLORS["text_primary"], font=("Segoe UI", 10))
        style.configure("TCombobox", fieldbackground=COLORS["surface_alt"], background=COLORS["surface_alt"], foreground=COLORS["text_primary"])

    def _build_main_layout(self):
        # Barra Superior de Status / Marca
        top_bar = tk.Frame(self.root, bg=COLORS["surface"], height=52, padx=20, pady=10)
        top_bar.pack(fill=tk.X, side=tk.TOP)

        brand_lbl = tk.Label(
            top_bar,
            text="PYTHON ULTIMATE CALCULATOR",
            font=("Segoe UI", 12, "bold"),
            fg=COLORS["accent_light"],
            bg=COLORS["surface"],
        )
        brand_lbl.pack(side=tk.LEFT)

        tag_lbl = tk.Label(
            top_bar,
            text="· Engenharia Científica, Financeira e Algébrica",
            font=("Segoe UI", 10),
            fg=COLORS["text_muted"],
            bg=COLORS["surface"],
        )
        tag_lbl.pack(side=tk.LEFT, padx=10)

        # Botão rápido para copiar visor
        copy_btn = tk.Button(
            top_bar,
            text="Copiar Resultado",
            font=("Segoe UI", 9, "bold"),
            bg=COLORS["surface_alt"],
            fg=COLORS["text_primary"],
            activebackground=COLORS["accent_primary"],
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=12,
            pady=4,
            command=self._copy_result_to_clipboard,
            cursor="hand2",
        )
        copy_btn.pack(side=tk.RIGHT)

        # Container Principal com Notebook (Abas)
        notebook_frame = tk.Frame(self.root, bg=COLORS["bg_dark"], padx=10, pady=10)
        notebook_frame.pack(fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Criação de cada aba especializada
        self.tab_calc = tk.Frame(self.notebook, bg=COLORS["surface"], padx=16, pady=16)
        self.tab_fractions = tk.Frame(self.notebook, bg=COLORS["surface"], padx=16, pady=16)
        self.tab_algebra = tk.Frame(self.notebook, bg=COLORS["surface"], padx=16, pady=16)
        self.tab_statistics = tk.Frame(self.notebook, bg=COLORS["surface"], padx=16, pady=16)
        self.tab_finance = tk.Frame(self.notebook, bg=COLORS["surface"], padx=16, pady=16)
        self.tab_converters = tk.Frame(self.notebook, bg=COLORS["surface"], padx=16, pady=16)
        self.tab_geometry = tk.Frame(self.notebook, bg=COLORS["surface"], padx=16, pady=16)
        self.tab_matrices = tk.Frame(self.notebook, bg=COLORS["surface"], padx=16, pady=16)
        self.tab_datetime = tk.Frame(self.notebook, bg=COLORS["surface"], padx=16, pady=16)
        self.tab_history = tk.Frame(self.notebook, bg=COLORS["surface"], padx=16, pady=16)

        self.notebook.add(self.tab_calc, text="Calculadora")
        self.notebook.add(self.tab_fractions, text="Frações & Teoria")
        self.notebook.add(self.tab_algebra, text="Álgebra")
        self.notebook.add(self.tab_statistics, text="Estatística")
        self.notebook.add(self.tab_finance, text="Financeiro")
        self.notebook.add(self.tab_converters, text="Conversores")
        self.notebook.add(self.tab_geometry, text="Geometria")
        self.notebook.add(self.tab_matrices, text="Matrizes & Vetores")
        self.notebook.add(self.tab_datetime, text="Data & Hora")
        self.notebook.add(self.tab_history, text="Histórico")

        # Constrói o conteúdo de cada módulo
        self._build_calc_tab()
        self._build_fractions_tab()
        self._build_algebra_tab()
        self._build_statistics_tab()
        self._build_finance_tab()
        self._build_converters_tab()
        self._build_geometry_tab()
        self._build_matrices_tab()
        self._build_datetime_tab()
        self._build_history_tab()

    # =========================================================================
    # 1. ABA CALCULADORA (BÁSICA E CIENTÍFICA)
    # =========================================================================

    def _build_calc_tab(self):
        container = tk.Frame(self.tab_calc, bg=COLORS["surface"])
        container.pack(fill=tk.BOTH, expand=True)

        # Painel do Visor (Display duplo: expressão em cima, resultado em destaque)
        display_panel = tk.Frame(container, bg=COLORS["bg_dark"], padx=16, pady=12, highlightbackground=COLORS["border"], highlightthickness=1)
        display_panel.pack(fill=tk.X, pady=(0, 14))

        # Indicador de Memória e Ângulo
        top_info = tk.Frame(display_panel, bg=COLORS["bg_dark"])
        top_info.pack(fill=tk.X)

        self.mem_indicator = tk.Label(top_info, text="", font=("Segoe UI", 9, "bold"), fg=COLORS["accent_light"], bg=COLORS["bg_dark"])
        self.mem_indicator.pack(side=tk.LEFT)

        angle_btn = tk.Button(
            top_info,
            textvariable=self.angle_mode_var,
            font=("Segoe UI", 9, "bold"),
            bg=COLORS["surface_alt"],
            fg=COLORS["text_primary"],
            relief=tk.FLAT,
            padx=8,
            pady=2,
            command=self._toggle_angle_mode,
            cursor="hand2",
        )
        angle_btn.pack(side=tk.RIGHT)

        # Entrada de Expressão
        self.expr_entry = tk.Entry(
            display_panel,
            textvariable=self.current_expr,
            font=("Consolas", 14),
            bg=COLORS["bg_dark"],
            fg=COLORS["text_muted"],
            relief=tk.FLAT,
            justify=tk.RIGHT,
            insertbackground="#ffffff",
        )
        self.expr_entry.pack(fill=tk.X, pady=(4, 2))

        # Visor Principal do Resultado
        self.result_lbl = tk.Label(
            display_panel,
            textvariable=self.display_result,
            font=("Consolas", 28, "bold"),
            bg=COLORS["bg_dark"],
            fg=COLORS["text_primary"],
            anchor="e",
        )
        self.result_lbl.pack(fill=tk.X)

        # Barra de Memória (MC, MR, M+, M-, MS)
        mem_bar = tk.Frame(container, bg=COLORS["surface"])
        mem_bar.pack(fill=tk.X, pady=(0, 10))

        mem_buttons = [
            ("MC", self._mem_clear),
            ("MR", self._mem_recall),
            ("M+", self._mem_add),
            ("M-", self._mem_sub),
            ("MS", self._mem_store),
        ]
        for label, cmd in mem_buttons:
            b = tk.Button(
                mem_bar,
                text=label,
                font=("Segoe UI", 9, "bold"),
                bg=COLORS["surface_alt"],
                fg=COLORS["accent_light"],
                activebackground=COLORS["accent_primary"],
                activeforeground="#ffffff",
                relief=tk.FLAT,
                width=6,
                pady=4,
                command=cmd,
                cursor="hand2",
            )
            b.pack(side=tk.LEFT, padx=3)

        # Grade de Botões Funcionais (Científica + Básica integradas)
        btn_grid = tk.Frame(container, bg=COLORS["surface"])
        btn_grid.pack(fill=tk.BOTH, expand=True)

        buttons_layout = [
            [("2nd", "sin", "cos", "tan", "π", "e"), ("CE", "C", "⌫", "÷")],
            [("x²", "xʸ", "√x", "ʸ√x", "log", "ln"), ("7", "8", "9", "×")],
            [("1/x", "|x|", "n!", "exp", "%", "("), ("4", "5", "6", "-")],
            [("sinh", "cosh", "tanh", "rad", "deg", ")"), ("1", "2", "3", "+")],
            [("round", "floor", "ceil", "mod", "comb", "perm"), ("±", "0", ",", "=")],
        ]

        # Configura colunas proporcionais
        for col in range(10):
            btn_grid.columnconfigure(col, weight=1)
        for row in range(5):
            btn_grid.rowconfigure(row, weight=1)

        for r_idx, row_data in enumerate(buttons_layout):
            sci_btns, basic_btns = row_data
            # Colunas 0 a 5: Botões científicos
            for c_idx, label in enumerate(sci_btns):
                self._create_calc_btn(btn_grid, label, r_idx, c_idx, is_sci=True)
            # Colunas 6 a 9: Botões básicos
            for c_idx, label in enumerate(basic_btns):
                self._create_calc_btn(btn_grid, label, r_idx, c_idx + 6, is_sci=False)

    def _create_calc_btn(self, parent, label: str, r: int, c: int, is_sci: bool = False):
        bg = COLORS["btn_fn_bg"] if is_sci else COLORS["btn_num_bg"]
        fg = COLORS["btn_fn_fg"] if is_sci else COLORS["btn_num_fg"]

        if label in ("÷", "×", "-", "+", "mod"):
            bg = COLORS["btn_op_bg"]
            fg = COLORS["btn_op_fg"]
        elif label == "=":
            bg = COLORS["btn_equal_bg"]
            fg = COLORS["btn_equal_fg"]
        elif label in ("C", "CE"):
            fg = COLORS["danger"]
        elif label in ("7", "8", "9", "4", "5", "6", "1", "2", "3", "0", ","):
            bg = COLORS["surface_alt"]
            fg = COLORS["text_primary"]

        btn = tk.Button(
            parent,
            text=label,
            font=("Segoe UI", 11, "bold"),
            bg=bg,
            fg=fg,
            activebackground=COLORS["accent_primary"],
            activeforeground="#ffffff",
            relief=tk.FLAT,
            command=lambda l=label: self._on_calc_btn_press(l),
            cursor="hand2",
        )
        btn.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")

    def _on_calc_btn_press(self, label: str):
        curr = self.current_expr.get()

        if label == "=":
            self._evaluate_calc()
        elif label == "C":
            self.current_expr.set("")
            self.display_result.set("0")
        elif label == "CE":
            self.current_expr.set("")
        elif label == "⌫":
            self.current_expr.set(curr[:-1])
        elif label == "±":
            res = self.display_result.get()
            toggled = CalculatorEngine.toggle_sign(res)
            self.display_result.set(toggled)
        elif label == "÷":
            self.current_expr.set(curr + " / ")
        elif label == "×":
            self.current_expr.set(curr + " * ")
        elif label == "mod":
            self.current_expr.set(curr + " % ")
        elif label == "π":
            self.current_expr.set(curr + "pi")
        elif label == "e":
            self.current_expr.set(curr + "e")
        elif label == "√x":
            self.current_expr.set(curr + "sqrt(")
        elif label == "x²":
            self.current_expr.set(curr + "^2")
        elif label == "xʸ":
            self.current_expr.set(curr + "^")
        elif label == "n!":
            self.current_expr.set(curr + "!")
        elif label == "1/x":
            try:
                val = float(self.display_result.get().replace(',', '.'))
                inv = 1.0 / val
                self.display_result.set(str(inv))
            except Exception as e:
                messagebox.showerror("Erro de Inverso", str(e))
        elif label in ("sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "log", "ln", "exp", "abs", "floor", "ceil", "round"):
            self.current_expr.set(curr + f"{label}(")
        else:
            self.current_expr.set(curr + label)

    def _evaluate_calc(self):
        expr = self.current_expr.get().strip()
        if not expr:
            return
        try:
            res_str, _ = self.engine.evaluate_expression(expr, category="Básica")
            self.display_result.set(res_str)
        except (ValidationError, MathDomainError) as err:
            self.display_result.set("Erro")
            messagebox.showerror("Erro de Cálculo", str(err))
        except Exception as err:
            self.display_result.set("Erro")
            messagebox.showerror("Erro Desconhecido", f"Ocorreu um erro: {err}")

    def _toggle_angle_mode(self):
        current = self.engine.angle_mode
        new_mode = "rad" if current == "deg" else "deg"
        self.engine.set_angle_mode(new_mode)
        self.angle_mode_var.set(new_mode.upper())

    def _mem_clear(self):
        self.engine.memory_clear()
        self.mem_indicator.config(text="")

    def _mem_recall(self):
        val = self.engine.memory_recall()
        self.current_expr.set(self.current_expr.get() + str(val))

    def _mem_add(self):
        try:
            val = float(self.display_result.get().replace(',', '.'))
            self.engine.memory_add(val)
            self.mem_indicator.config(text="M")
        except ValueError:
            pass

    def _mem_sub(self):
        try:
            val = float(self.display_result.get().replace(',', '.'))
            self.engine.memory_subtract(val)
            self.mem_indicator.config(text="M")
        except ValueError:
            pass

    def _mem_store(self):
        try:
            val = float(self.display_result.get().replace(',', '.'))
            self.engine.memory_store(val)
            self.mem_indicator.config(text="M")
        except ValueError:
            pass

    def _copy_result_to_clipboard(self):
        res = self.display_result.get()
        self.root.clipboard_clear()
        self.root.clipboard_append(res)
        messagebox.showinfo("Copiado", f"Resultado '{res}' copiado para a área de transferência.")

    # =========================================================================
    # 2. ABA FRAÇÕES E ARITMÉTICA
    # =========================================================================

    def _build_fractions_tab(self):
        f = self.tab_fractions
        lbl = tk.Label(f, text="Aritmética de Frações e Teoria dos Números", font=("Segoe UI", 14, "bold"), fg=COLORS["accent_light"], bg=COLORS["surface"])
        lbl.pack(anchor="w", pady=(0, 15))

        # Frame de Operações com Frações
        op_box = tk.LabelFrame(f, text="Operações com Duas Frações", bg=COLORS["surface"], fg=COLORS["text_primary"], padx=10, pady=10)
        op_box.pack(fill=tk.X, pady=(0, 15))

        row1 = tk.Frame(op_box, bg=COLORS["surface"])
        row1.pack(fill=tk.X, pady=4)

        tk.Label(row1, text="Fração 1 (num/den):", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.f1_num = tk.Entry(row1, width=6, bg=COLORS["surface_alt"], fg="#ffffff")
        self.f1_num.pack(side=tk.LEFT, padx=3)
        self.f1_num.insert(0, "3")
        tk.Label(row1, text="/", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.f1_den = tk.Entry(row1, width=6, bg=COLORS["surface_alt"], fg="#ffffff")
        self.f1_den.pack(side=tk.LEFT, padx=3)
        self.f1_den.insert(0, "4")

        tk.Label(row1, text="  Operação:", bg=COLORS["surface"]).pack(side=tk.LEFT, padx=5)
        self.frac_op_var = tk.StringVar(value="+")
        op_menu = ttk.Combobox(row1, textvariable=self.frac_op_var, values=["+", "-", "×", "÷"], width=4, state="readonly")
        op_menu.pack(side=tk.LEFT, padx=3)

        tk.Label(row1, text="  Fração 2 (num/den):", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.f2_num = tk.Entry(row1, width=6, bg=COLORS["surface_alt"], fg="#ffffff")
        self.f2_num.pack(side=tk.LEFT, padx=3)
        self.f2_num.insert(0, "2")
        tk.Label(row1, text="/", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.f2_den = tk.Entry(row1, width=6, bg=COLORS["surface_alt"], fg="#ffffff")
        self.f2_den.pack(side=tk.LEFT, padx=3)
        self.f2_den.insert(0, "5")

        calc_frac_btn = tk.Button(row1, text="Calcular Frações", bg=COLORS["accent_primary"], fg="#ffffff", padx=10, relief=tk.FLAT, command=self._calc_fractions)
        calc_frac_btn.pack(side=tk.LEFT, padx=15)

        self.frac_res_lbl = tk.Label(op_box, text="Resultado: -", font=("Consolas", 12, "bold"), fg=COLORS["accent_light"], bg=COLORS["surface"])
        self.frac_res_lbl.pack(anchor="w", pady=(8, 0))

        # MDC e MMC
        mdc_box = tk.LabelFrame(f, text="MDC, MMC e Fatoração Prima", bg=COLORS["surface"], fg=COLORS["text_primary"], padx=10, pady=10)
        mdc_box.pack(fill=tk.X, pady=(0, 15))

        r2 = tk.Frame(mdc_box, bg=COLORS["surface"])
        r2.pack(fill=tk.X, pady=4)

        tk.Label(r2, text="Lista de números (separados por vírgula):", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.mdc_entry = tk.Entry(r2, width=24, bg=COLORS["surface_alt"], fg="#ffffff")
        self.mdc_entry.pack(side=tk.LEFT, padx=8)
        self.mdc_entry.insert(0, "24, 36, 60")

        tk.Button(r2, text="Calcular MDC/MMC", bg=COLORS["accent_primary"], fg="#ffffff", relief=tk.FLAT, command=self._calc_mdc_mmc).pack(side=tk.LEFT, padx=5)

        self.mdc_res_lbl = tk.Label(mdc_box, text="MDC = - | MMC = -", font=("Consolas", 11, "bold"), fg=COLORS["text_primary"], bg=COLORS["surface"])
        self.mdc_res_lbl.pack(anchor="w", pady=(6, 0))

        # Primalidade e Fatores
        r3 = tk.Frame(mdc_box, bg=COLORS["surface"])
        r3.pack(fill=tk.X, pady=(10, 4))

        tk.Label(r3, text="Número inteiro para analisar:", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.prime_entry = tk.Entry(r3, width=12, bg=COLORS["surface_alt"], fg="#ffffff")
        self.prime_entry.pack(side=tk.LEFT, padx=8)
        self.prime_entry.insert(0, "84")

        tk.Button(r3, text="Verificar Primalidade & Divisores", bg=COLORS["surface_alt"], fg=COLORS["accent_light"], relief=tk.FLAT, command=self._calc_prime_info).pack(side=tk.LEFT, padx=5)

        self.prime_res_lbl = tk.Label(mdc_box, text="", font=("Consolas", 10), fg=COLORS["text_muted"], bg=COLORS["surface"], justify=tk.LEFT)
        self.prime_res_lbl.pack(anchor="w", pady=(6, 0))

    def _calc_fractions(self):
        try:
            n1 = int(self.f1_num.get())
            d1 = int(self.f1_den.get())
            n2 = int(self.f2_num.get())
            d2 = int(self.f2_den.get())
            op = self.frac_op_var.get()

            if op == "+":
                num, den = FractionsMath.add_fractions(n1, d1, n2, d2)
            elif op == "-":
                num, den = FractionsMath.subtract_fractions(n1, d1, n2, d2)
            elif op == "×":
                num, den = FractionsMath.multiply_fractions(n1, d1, n2, d2)
            else:
                num, den = FractionsMath.divide_fractions(n1, d1, n2, d2)

            dec = FractionsMath.fraction_to_decimal(num, den)
            self.frac_res_lbl.config(text=f"Resultado: {num}/{den}  (Decimal: {dec:.6g})")
            self.history_mgr.add_entry(f"({n1}/{d1}) {op} ({n2}/{d2})", f"{num}/{den} = {dec:.6g}", "Frações")
        except Exception as e:
            messagebox.showerror("Erro em Frações", str(e))

    def _calc_mdc_mmc(self):
        try:
            raw = self.mdc_entry.get().split(',')
            nums = [int(x.strip()) for x in raw if x.strip()]
            g = FractionsMath.gcd_multiple(nums)
            l = FractionsMath.lcm_multiple(nums)
            self.mdc_res_lbl.config(text=f"MDC({nums}) = {g}  |  MMC({nums}) = {l}")
            self.history_mgr.add_entry(f"MDC/MMC de {nums}", f"MDC={g}, MMC={l}", "Aritmética")
        except Exception as e:
            messagebox.showerror("Erro MDC/MMC", str(e))

    def _calc_prime_info(self):
        try:
            n = int(self.prime_entry.get().strip())
            is_p = FractionsMath.is_prime(n)
            divs = FractionsMath.get_divisors(n)
            status = "É PRIMO" if is_p else "NÃO É PRIMO (Composto)"
            fact_str = ""
            if n > 1 and not is_p:
                factors = FractionsMath.prime_factors(n)
                fact_str = " · ".join([f"{p}^{exp}" if exp > 1 else f"{p}" for p, exp in factors.items()])
                fact_str = f"\nFatoração Prima: {n} = {fact_str}"

            divs_str = ", ".join(map(str, divs[:30]))
            if len(divs) > 30:
                divs_str += f"... (+{len(divs) - 30} divisores)"

            txt = f"Diagnóstico: {n} {status}{fact_str}\nTotal de divisores: {len(divs)} -> [{divs_str}]"
            self.prime_res_lbl.config(text=txt)
        except Exception as e:
            messagebox.showerror("Erro Primalidade", str(e))

    # =========================================================================
    # 3. ABA ÁLGEBRA
    # =========================================================================

    def _build_algebra_tab(self):
        f = self.tab_algebra
        tk.Label(f, text="Solucionador Algébrico com Passo a Passo", font=("Segoe UI", 14, "bold"), fg=COLORS["accent_light"], bg=COLORS["surface"]).pack(anchor="w", pady=(0, 15))

        # Equação de 2º Grau
        quad_box = tk.LabelFrame(f, text="Equação do 2º Grau (ax² + bx + c = 0)", bg=COLORS["surface"], fg=COLORS["text_primary"], padx=10, pady=10)
        quad_box.pack(fill=tk.X, pady=(0, 10))

        q_row = tk.Frame(quad_box, bg=COLORS["surface"])
        q_row.pack(fill=tk.X, pady=4)

        tk.Label(q_row, text="a:", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.quad_a = tk.Entry(q_row, width=5, bg=COLORS["surface_alt"], fg="#ffffff")
        self.quad_a.pack(side=tk.LEFT, padx=3)
        self.quad_a.insert(0, "1")

        tk.Label(q_row, text="b:", bg=COLORS["surface"]).pack(side=tk.LEFT, padx=(6, 0))
        self.quad_b = tk.Entry(q_row, width=5, bg=COLORS["surface_alt"], fg="#ffffff")
        self.quad_b.pack(side=tk.LEFT, padx=3)
        self.quad_b.insert(0, "-5")

        tk.Label(q_row, text="c:", bg=COLORS["surface"]).pack(side=tk.LEFT, padx=(6, 0))
        self.quad_c = tk.Entry(q_row, width=5, bg=COLORS["surface_alt"], fg="#ffffff")
        self.quad_c.pack(side=tk.LEFT, padx=3)
        self.quad_c.insert(0, "6")

        tk.Button(q_row, text="Resolver Equação", bg=COLORS["accent_primary"], fg="#ffffff", relief=tk.FLAT, command=self._solve_quadratic).pack(side=tk.LEFT, padx=12)

        self.quad_res_txt = tk.Text(quad_box, height=5, bg=COLORS["bg_dark"], fg=COLORS["text_primary"], font=("Consolas", 10), relief=tk.FLAT)
        self.quad_res_txt.pack(fill=tk.X, pady=(6, 0))

        # Sistemas Lineares 2x2
        sys_box = tk.LabelFrame(f, text="Sistema Linear 2x2 (a₁x + b₁y = c₁  e  a₂x + b₂y = c₂)", bg=COLORS["surface"], fg=COLORS["text_primary"], padx=10, pady=10)
        sys_box.pack(fill=tk.X, pady=(0, 10))

        s_r1 = tk.Frame(sys_box, bg=COLORS["surface"])
        s_r1.pack(fill=tk.X, pady=2)
        tk.Label(s_r1, text="Eq 1: ", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.sys_a1 = tk.Entry(s_r1, width=4, bg=COLORS["surface_alt"], fg="#ffffff"); self.sys_a1.pack(side=tk.LEFT); self.sys_a1.insert(0, "2")
        tk.Label(s_r1, text="x +", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.sys_b1 = tk.Entry(s_r1, width=4, bg=COLORS["surface_alt"], fg="#ffffff"); self.sys_b1.pack(side=tk.LEFT); self.sys_b1.insert(0, "1")
        tk.Label(s_r1, text="y = ", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.sys_c1 = tk.Entry(s_r1, width=4, bg=COLORS["surface_alt"], fg="#ffffff"); self.sys_c1.pack(side=tk.LEFT); self.sys_c1.insert(0, "7")

        s_r2 = tk.Frame(sys_box, bg=COLORS["surface"])
        s_r2.pack(fill=tk.X, pady=2)
        tk.Label(s_r2, text="Eq 2: ", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.sys_a2 = tk.Entry(s_r2, width=4, bg=COLORS["surface_alt"], fg="#ffffff"); self.sys_a2.pack(side=tk.LEFT); self.sys_a2.insert(0, "1")
        tk.Label(s_r2, text="x -", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.sys_b2 = tk.Entry(s_r2, width=4, bg=COLORS["surface_alt"], fg="#ffffff"); self.sys_b2.pack(side=tk.LEFT); self.sys_b2.insert(0, "-1")
        tk.Label(s_r2, text="y = ", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.sys_c2 = tk.Entry(s_r2, width=4, bg=COLORS["surface_alt"], fg="#ffffff"); self.sys_c2.pack(side=tk.LEFT); self.sys_c2.insert(0, "1")

        tk.Button(s_r2, text="Resolver Sistema", bg=COLORS["accent_primary"], fg="#ffffff", relief=tk.FLAT, command=self._solve_linear_system).pack(side=tk.LEFT, padx=12)

        self.sys_res_txt = tk.Text(sys_box, height=4, bg=COLORS["bg_dark"], fg=COLORS["text_primary"], font=("Consolas", 10), relief=tk.FLAT)
        self.sys_res_txt.pack(fill=tk.X, pady=(6, 0))

    def _solve_quadratic(self):
        try:
            a = float(self.quad_a.get())
            b = float(self.quad_b.get())
            c = float(self.quad_c.get())
            res = AlgebraSolver.solve_quadratic_equation(a, b, c)
            self.quad_res_txt.delete("1.0", tk.END)
            self.quad_res_txt.insert(tk.END, "\n".join(res["passos"]))
            self.history_mgr.add_entry(f"{a}x² + {b}x + {c} = 0", f"x1={res['x1_str']}, x2={res['x2_str']}", "Álgebra")
        except Exception as e:
            messagebox.showerror("Erro Álgebra", str(e))

    def _solve_linear_system(self):
        try:
            a1 = float(self.sys_a1.get())
            b1 = float(self.sys_b1.get())
            c1 = float(self.sys_c1.get())
            a2 = float(self.sys_a2.get())
            b2 = float(self.sys_b2.get())
            c2 = float(self.sys_c2.get())
            res = AlgebraSolver.solve_linear_system_2x2(a1, b1, c1, a2, b2, c2)
            self.sys_res_txt.delete("1.0", tk.END)
            self.sys_res_txt.insert(tk.END, "\n".join(res["passos"]))
            res_str = f"x={res['x']}, y={res['y']}" if res["x"] is not None else res["descricao"]
            self.history_mgr.add_entry(f"Sistema 2x2 [{a1}x+{b1}y={c1}; {a2}x+{b2}y={c2}]", res_str, "Álgebra")
        except Exception as e:
            messagebox.showerror("Erro Sistema Linear", str(e))

    # =========================================================================
    # 4. ABA ESTATÍSTICA E PROBABILIDADE
    # =========================================================================

    def _build_statistics_tab(self):
        f = self.tab_statistics
        tk.Label(f, text="Estatística Descritiva e Probabilidade", font=("Segoe UI", 14, "bold"), fg=COLORS["accent_light"], bg=COLORS["surface"]).pack(anchor="w", pady=(0, 10))

        tk.Label(f, text="Insira a amostra de dados (separados por vírgula, espaço ou ponto e vírgula):", bg=COLORS["surface"], fg=COLORS["text_muted"]).pack(anchor="w")
        self.stats_entry = tk.Entry(f, bg=COLORS["surface_alt"], fg="#ffffff", font=("Consolas", 11))
        self.stats_entry.pack(fill=tk.X, pady=(4, 10))
        self.stats_entry.insert(0, "12, 15, 12, 18, 22, 19, 15, 24, 30, 15")

        btn_row = tk.Frame(f, bg=COLORS["surface"])
        btn_row.pack(fill=tk.X, pady=(0, 10))
        tk.Button(btn_row, text="Calcular Estatísticas", bg=COLORS["accent_primary"], fg="#ffffff", padx=12, relief=tk.FLAT, command=self._calc_statistics).pack(side=tk.LEFT)

        self.stats_out_txt = tk.Text(f, height=14, bg=COLORS["bg_dark"], fg=COLORS["text_primary"], font=("Consolas", 10), relief=tk.FLAT)
        self.stats_out_txt.pack(fill=tk.BOTH, expand=True)

    def _calc_statistics(self):
        try:
            raw = self.stats_entry.get()
            data = StatisticsEngine.parse_data_series(raw)
            desc = StatisticsEngine.descriptive_analysis(data)

            lines = [
                f"--- ANÁLISE DESCRITIVA DA AMOSTRA (N = {desc['n']}) ---",
                f"Média Aritmética:          {desc['media']}",
                f"Mediana:                   {desc['mediana']}",
                f"Moda:                      {'Amodal' if desc['amodal'] else ', '.join(map(str, desc['modas']))}",
                f"Mínimo / Máximo:           {desc['minimo']} / {desc['maximo']}",
                f"Amplitude Total:           {desc['amplitude']}",
                f"Variância Amostral (s²):   {desc['variancia_amostral']}",
                f"Desvio-Padrão Amostral (s):{desc['desvio_padrao_amostral']}",
                f"Desvio-Padrão Pop. (σ):    {desc['desvio_padrao_populacional']}",
                f"Quartis (Q1 / Q2 / Q3):    {desc['q1']} / {desc['q2']} / {desc['q3']} (IQR: {desc['iqr']})",
                "",
                "--- TABELA DE FREQUÊNCIA ABSOLUTA E RELATIVA ---",
            ]
            for row in desc["distribuicao"]:
                lines.append(f"  Valor {row['valor']:>8}: Freq = {row['frequencia_absoluta']:<3} ({row['frequencia_relativa_pct']:>5.2f}%)")

            self.stats_out_txt.delete("1.0", tk.END)
            self.stats_out_txt.insert(tk.END, "\n".join(lines))
            self.history_mgr.add_entry(f"Estatística de N={desc['n']}", f"Média={desc['media']}, DP={desc['desvio_padrao_amostral']}", "Estatística")
        except Exception as e:
            messagebox.showerror("Erro Estatístico", str(e))

    # =========================================================================
    # 5. ABA FINANCEIRO
    # =========================================================================

    def _build_finance_tab(self):
        f = self.tab_finance
        tk.Label(f, text="Matemática Financeira de Alta Precisão (Decimal)", font=("Segoe UI", 14, "bold"), fg=COLORS["accent_light"], bg=COLORS["surface"]).pack(anchor="w", pady=(0, 10))

        # Financiamento Price
        price_box = tk.LabelFrame(f, text="Financiamento / Empréstimo com Parcelas Fixas (Tabela Price)", bg=COLORS["surface"], fg=COLORS["text_primary"], padx=10, pady=10)
        price_box.pack(fill=tk.X, pady=(0, 10))

        p_row = tk.Frame(price_box, bg=COLORS["surface"])
        p_row.pack(fill=tk.X)

        tk.Label(p_row, text="Valor (R$):", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.fin_pv = tk.Entry(p_row, width=10, bg=COLORS["surface_alt"], fg="#ffffff"); self.fin_pv.pack(side=tk.LEFT, padx=3); self.fin_pv.insert(0, "10000")

        tk.Label(p_row, text="Taxa Mensal (%):", bg=COLORS["surface"]).pack(side=tk.LEFT, padx=(8, 0))
        self.fin_rate = tk.Entry(p_row, width=6, bg=COLORS["surface_alt"], fg="#ffffff"); self.fin_rate.pack(side=tk.LEFT, padx=3); self.fin_rate.insert(0, "1.5")

        tk.Label(p_row, text="Parcelas:", bg=COLORS["surface"]).pack(side=tk.LEFT, padx=(8, 0))
        self.fin_n = tk.Entry(p_row, width=5, bg=COLORS["surface_alt"], fg="#ffffff"); self.fin_n.pack(side=tk.LEFT, padx=3); self.fin_n.insert(0, "24")

        tk.Button(p_row, text="Calcular Parcelas", bg=COLORS["accent_primary"], fg="#ffffff", relief=tk.FLAT, command=self._calc_financing).pack(side=tk.LEFT, padx=12)

        self.fin_res_lbl = tk.Label(price_box, text="Parcela Fixa: - | Total Pago: - | Total Juros: -", font=("Consolas", 11, "bold"), fg=COLORS["accent_light"], bg=COLORS["surface"])
        self.fin_res_lbl.pack(anchor="w", pady=(8, 0))

        # Margem vs Markup
        margin_box = tk.LabelFrame(f, text="Margem de Lucro vs Markup Comercial", bg=COLORS["surface"], fg=COLORS["text_primary"], padx=10, pady=10)
        margin_box.pack(fill=tk.X, pady=(0, 10))

        m_row = tk.Frame(margin_box, bg=COLORS["surface"])
        m_row.pack(fill=tk.X)

        tk.Label(m_row, text="Custo do Produto (R$):", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.mk_cost = tk.Entry(m_row, width=8, bg=COLORS["surface_alt"], fg="#ffffff"); self.mk_cost.pack(side=tk.LEFT, padx=3); self.mk_cost.insert(0, "50")

        tk.Label(m_row, text="Preço de Venda (R$):", bg=COLORS["surface"]).pack(side=tk.LEFT, padx=(8, 0))
        self.mk_pv = tk.Entry(m_row, width=8, bg=COLORS["surface_alt"], fg="#ffffff"); self.mk_pv.pack(side=tk.LEFT, padx=3); self.mk_pv.insert(0, "85")

        tk.Button(m_row, text="Analisar Margem/Markup", bg=COLORS["surface_alt"], fg=COLORS["accent_light"], relief=tk.FLAT, command=self._calc_markup).pack(side=tk.LEFT, padx=12)

        self.mk_res_lbl = tk.Label(margin_box, text="Lucro: - | Margem de Lucro: - | Markup: -", font=("Consolas", 11, "bold"), fg=COLORS["text_primary"], bg=COLORS["surface"])
        self.mk_res_lbl.pack(anchor="w", pady=(8, 0))

        # Investimentos Mensais
        inv_box = tk.LabelFrame(f, text="Simulação de Investimentos com Aportes Mensais", bg=COLORS["surface"], fg=COLORS["text_primary"], padx=10, pady=10)
        inv_box.pack(fill=tk.X, pady=(0, 10))

        i_row = tk.Frame(inv_box, bg=COLORS["surface"])
        i_row.pack(fill=tk.X)

        tk.Label(i_row, text="Inicial:", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.inv_ini = tk.Entry(i_row, width=8, bg=COLORS["surface_alt"], fg="#ffffff"); self.inv_ini.pack(side=tk.LEFT, padx=3); self.inv_ini.insert(0, "1000")

        tk.Label(i_row, text="Aporte Mensal:", bg=COLORS["surface"]).pack(side=tk.LEFT, padx=(6, 0))
        self.inv_dep = tk.Entry(i_row, width=8, bg=COLORS["surface_alt"], fg="#ffffff"); self.inv_dep.pack(side=tk.LEFT, padx=3); self.inv_dep.insert(0, "300")

        tk.Label(i_row, text="Taxa Mês (%):", bg=COLORS["surface"]).pack(side=tk.LEFT, padx=(6, 0))
        self.inv_rate = tk.Entry(i_row, width=5, bg=COLORS["surface_alt"], fg="#ffffff"); self.inv_rate.pack(side=tk.LEFT, padx=3); self.inv_rate.insert(0, "0.8")

        tk.Label(i_row, text="Meses:", bg=COLORS["surface"]).pack(side=tk.LEFT, padx=(6, 0))
        self.inv_months = tk.Entry(i_row, width=5, bg=COLORS["surface_alt"], fg="#ffffff"); self.inv_months.pack(side=tk.LEFT, padx=3); self.inv_months.insert(0, "36")

        tk.Button(i_row, text="Simular", bg=COLORS["accent_primary"], fg="#ffffff", relief=tk.FLAT, command=self._calc_investment).pack(side=tk.LEFT, padx=10)

        self.inv_res_lbl = tk.Label(inv_box, text="Total Investido: - | Saldo Final Acumulado: - | Juros Recebidos: -", font=("Consolas", 11, "bold"), fg=COLORS["accent_light"], bg=COLORS["surface"])
        self.inv_res_lbl.pack(anchor="w", pady=(8, 0))

    def _calc_financing(self):
        try:
            pv = self.fin_pv.get()
            rate = self.fin_rate.get()
            n = int(self.fin_n.get())
            res = FinanceEngine.price_table_financing(pv, rate, n)
            self.fin_res_lbl.config(
                text=f"Parcela Fixa: {res['valor_parcela_fmt']}  |  Total Pago: {res['total_pago_fmt']}  |  Juros Totais: {res['total_juros_fmt']}"
            )
            self.history_mgr.add_entry(f"Financiamento R$ {pv} em {n}x a {rate}%/mês", f"Parcela {res['valor_parcela_fmt']}", "Financeiro")
        except Exception as e:
            messagebox.showerror("Erro Financeiro", str(e))

    def _calc_markup(self):
        try:
            c = self.mk_cost.get()
            pv = self.mk_pv.get()
            res = FinanceEngine.margin_and_markup(c, pv)
            self.mk_res_lbl.config(
                text=f"Lucro Bruto: {res['lucro_bruto_fmt']}  |  Margem de Lucro: {res['margem_lucro_pct']}%  |  Markup: {res['markup_pct']}%"
            )
        except Exception as e:
            messagebox.showerror("Erro Margem/Markup", str(e))

    def _calc_investment(self):
        try:
            ini = self.inv_ini.get()
            dep = self.inv_dep.get()
            rate = self.inv_rate.get()
            months = int(self.inv_months.get())
            res = FinanceEngine.investment_with_monthly_contributions(ini, dep, rate, months)
            self.inv_res_lbl.config(
                text=f"Total Investido: {res['total_investido_fmt']}  |  Saldo Final: {res['saldo_final_fmt']}  |  Rendimento Juros: {res['juros_acumulados_fmt']}"
            )
        except Exception as e:
            messagebox.showerror("Erro Investimento", str(e))

    # =========================================================================
    # 6. ABA CONVERSORES DE UNIDADES
    # =========================================================================

    def _build_converters_tab(self):
        f = self.tab_converters
        tk.Label(f, text="Conversor de Grandezas Físicas e Digitais", font=("Segoe UI", 14, "bold"), fg=COLORS["accent_light"], bg=COLORS["surface"]).pack(anchor="w", pady=(0, 15))

        top_ctrl = tk.Frame(f, bg=COLORS["surface"])
        top_ctrl.pack(fill=tk.X, pady=(0, 15))

        tk.Label(top_ctrl, text="Categoria de Conversão:", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.conv_cats = [
            "Comprimento", "Massa", "Temperatura", "Tempo", "Área",
            "Volume", "Velocidade", "Dados Digitais (MB vs MiB)", "Energia", "Pressão", "Ângulos"
        ]
        self.conv_cat_var = tk.StringVar(value=self.conv_cats[0])
        self.cat_menu = ttk.Combobox(top_ctrl, textvariable=self.conv_cat_var, values=self.conv_cats, state="readonly", width=28)
        self.cat_menu.pack(side=tk.LEFT, padx=10)
        self.cat_menu.bind("<<ComboboxSelected>>", self._on_conv_cat_change)

        box = tk.LabelFrame(f, text="Parâmetros de Conversão", bg=COLORS["surface"], fg=COLORS["text_primary"], padx=15, pady=15)
        box.pack(fill=tk.X)

        r = tk.Frame(box, bg=COLORS["surface"])
        r.pack(fill=tk.X, pady=8)

        tk.Label(r, text="Valor:", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.conv_val_entry = tk.Entry(r, width=12, bg=COLORS["surface_alt"], fg="#ffffff")
        self.conv_val_entry.pack(side=tk.LEFT, padx=5)
        self.conv_val_entry.insert(0, "100")

        tk.Label(r, text="De:", bg=COLORS["surface"]).pack(side=tk.LEFT, padx=(10, 0))
        self.conv_from_var = tk.StringVar()
        self.conv_from_menu = ttk.Combobox(r, textvariable=self.conv_from_var, state="readonly", width=10)
        self.conv_from_menu.pack(side=tk.LEFT, padx=5)

        tk.Label(r, text="Para:", bg=COLORS["surface"]).pack(side=tk.LEFT, padx=(10, 0))
        self.conv_to_var = tk.StringVar()
        self.conv_to_menu = ttk.Combobox(r, textvariable=self.conv_to_var, state="readonly", width=10)
        self.conv_to_menu.pack(side=tk.LEFT, padx=5)

        tk.Button(r, text="Converter Agora", bg=COLORS["accent_primary"], fg="#ffffff", padx=12, relief=tk.FLAT, command=self._execute_conversion).pack(side=tk.LEFT, padx=15)

        self.conv_res_lbl = tk.Label(box, text="Resultado da Conversão: -", font=("Consolas", 14, "bold"), fg=COLORS["accent_light"], bg=COLORS["surface"])
        self.conv_res_lbl.pack(anchor="w", pady=(15, 5))

        self.conv_note_lbl = tk.Label(box, text="", font=("Segoe UI", 9), fg=COLORS["text_muted"], bg=COLORS["surface"])
        self.conv_note_lbl.pack(anchor="w")

        self._on_conv_cat_change()

    def _on_conv_cat_change(self, event=None):
        cat = self.conv_cat_var.get()
        units_map = {
            "Comprimento": ["m", "cm", "mm", "km", "in", "ft", "yd", "mi"],
            "Massa": ["kg", "g", "mg", "t", "lb", "oz"],
            "Temperatura": ["C", "F", "K"],
            "Tempo": ["s", "ms", "min", "h", "d", "sem"],
            "Área": ["m2", "cm2", "mm2", "ha", "km2"],
            "Volume": ["l", "ml", "m3", "gal"],
            "Velocidade": ["km/h", "m/s", "mph"],
            "Dados Digitais (MB vs MiB)": ["MB", "MiB", "GB", "GiB", "KB", "KiB", "B", "bit", "TB", "TiB"],
            "Energia": ["J", "kJ", "kWh", "cal", "kcal"],
            "Pressão": ["Pa", "kPa", "bar", "atm", "psi"],
            "Ângulos": ["deg", "rad", "grad"],
        }
        units = units_map.get(cat, ["m", "cm"])
        self.conv_from_menu.config(values=units)
        self.conv_to_menu.config(values=units)
        self.conv_from_var.set(units[0])
        self.conv_to_var.set(units[1] if len(units) > 1 else units[0])

        if "Dados Digitais" in cat:
            self.conv_note_lbl.config(text="Nota: 1 MB (SI decimal) = 1.000.000 B | 1 MiB (IEC binário) = 1.048.576 B (1024²).")
        else:
            self.conv_note_lbl.config(text="")

    def _execute_conversion(self):
        try:
            val = float(self.conv_val_entry.get().replace(',', '.'))
            cat = self.conv_cat_var.get()
            u_from = self.conv_from_var.get()
            u_to = self.conv_to_var.get()

            if cat == "Comprimento":
                res = UnitConverter.convert_length(val, u_from, u_to)
            elif cat == "Massa":
                res = UnitConverter.convert_mass(val, u_from, u_to)
            elif cat == "Temperatura":
                res = UnitConverter.convert_temperature(val, u_from, u_to)
            elif cat == "Tempo":
                res = UnitConverter.convert_time(val, u_from, u_to)
            elif cat == "Área":
                res = UnitConverter.convert_area(val, u_from, u_to)
            elif cat == "Volume":
                res = UnitConverter.convert_volume(val, u_from, u_to)
            elif cat == "Velocidade":
                res = UnitConverter.convert_speed(val, u_from, u_to)
            elif "Dados Digitais" in cat:
                res = UnitConverter.convert_digital_data(val, u_from, u_to)
            elif cat == "Energia":
                res = UnitConverter.convert_energy(val, u_from, u_to)
            elif cat == "Pressão":
                res = UnitConverter.convert_pressure(val, u_from, u_to)
            elif cat == "Ângulos":
                res = UnitConverter.convert_angle(val, u_from, u_to)
            else:
                res = val

            self.conv_res_lbl.config(text=f"{val} {u_from} = {res:.6g} {u_to}")
            self.history_mgr.add_entry(f"Conversão {val} {u_from} -> {u_to}", f"{res:.6g} {u_to}", "Conversão")
        except Exception as e:
            messagebox.showerror("Erro de Conversão", str(e))

    # =========================================================================
    # 7. ABA GEOMETRIA
    # =========================================================================

    def _build_geometry_tab(self):
        f = self.tab_geometry
        tk.Label(f, text="Geometria Plana, Espacial e Teorema de Pitágoras", font=("Segoe UI", 14, "bold"), fg=COLORS["accent_light"], bg=COLORS["surface"]).pack(anchor="w", pady=(0, 10))

        # Pitágoras
        pit_box = tk.LabelFrame(f, text="Teorema de Pitágoras (a² + b² = c²)", bg=COLORS["surface"], fg=COLORS["text_primary"], padx=10, pady=10)
        pit_box.pack(fill=tk.X, pady=(0, 10))

        p_r = tk.Frame(pit_box, bg=COLORS["surface"])
        p_r.pack(fill=tk.X)
        tk.Label(p_r, text="Cateto a:", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.pit_a = tk.Entry(p_r, width=6, bg=COLORS["surface_alt"], fg="#ffffff"); self.pit_a.pack(side=tk.LEFT, padx=3); self.pit_a.insert(0, "3")
        tk.Label(p_r, text="Cateto b:", bg=COLORS["surface"]).pack(side=tk.LEFT, padx=(6, 0))
        self.pit_b = tk.Entry(p_r, width=6, bg=COLORS["surface_alt"], fg="#ffffff"); self.pit_b.pack(side=tk.LEFT, padx=3); self.pit_b.insert(0, "4")
        tk.Button(p_r, text="Calcular Hipotenusa (c)", bg=COLORS["accent_primary"], fg="#ffffff", relief=tk.FLAT, command=self._calc_pitagoras).pack(side=tk.LEFT, padx=12)

        self.pit_res = tk.Label(pit_box, text="Hipotenusa: c = -", font=("Consolas", 11, "bold"), fg=COLORS["accent_light"], bg=COLORS["surface"])
        self.pit_res.pack(anchor="w", pady=(6, 0))

        # Círculo e Esfera
        circ_box = tk.LabelFrame(f, text="Círculo (2D) e Esfera (3D)", bg=COLORS["surface"], fg=COLORS["text_primary"], padx=10, pady=10)
        circ_box.pack(fill=tk.X, pady=(0, 10))

        c_r = tk.Frame(circ_box, bg=COLORS["surface"])
        c_r.pack(fill=tk.X)
        tk.Label(c_r, text="Raio (r):", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.geo_r = tk.Entry(c_r, width=8, bg=COLORS["surface_alt"], fg="#ffffff"); self.geo_r.pack(side=tk.LEFT, padx=3); self.geo_r.insert(0, "5")
        tk.Button(c_r, text="Calcular Círculo & Esfera", bg=COLORS["surface_alt"], fg=COLORS["accent_light"], relief=tk.FLAT, command=self._calc_circle_sphere).pack(side=tk.LEFT, padx=12)

        self.circ_res = tk.Label(circ_box, text="Área Círculo: - | Circunferência: - | Volume Esfera: -", font=("Consolas", 11, "bold"), fg=COLORS["text_primary"], bg=COLORS["surface"])
        self.circ_res.pack(anchor="w", pady=(6, 0))

    def _calc_pitagoras(self):
        try:
            a = float(self.pit_a.get())
            b = float(self.pit_b.get())
            res = GeometryCalculator.pythagoras_hypotenuse(a, b)
            self.pit_res.config(text=f"Hipotenusa c = {res['hipotenusa']:.4f}  ({res['passos']})")
        except Exception as e:
            messagebox.showerror("Erro Pitágoras", str(e))

    def _calc_circle_sphere(self):
        try:
            r = float(self.geo_r.get())
            c = GeometryCalculator.circle(r)
            s = GeometryCalculator.sphere(r)
            self.circ_res.config(
                text=f"Círculo: Área={c['area']:.4f}, Circ={c['circunferencia']:.4f}  |  Esfera: Vol={s['volume']:.4f}, Sup={s['area_superficial']:.4f}"
            )
        except Exception as e:
            messagebox.showerror("Erro Geometria", str(e))

    # =========================================================================
    # 8. ABA MATRIZES E VETORES
    # =========================================================================

    def _build_matrices_tab(self):
        f = self.tab_matrices
        tk.Label(f, text="Álgebra Linear: Matrizes e Vetores", font=("Segoe UI", 14, "bold"), fg=COLORS["accent_light"], bg=COLORS["surface"]).pack(anchor="w", pady=(0, 10))

        tk.Label(f, text="Matriz A (linhas separadas por quebra de linha, colunas por espaço):", bg=COLORS["surface"], fg=COLORS["text_muted"]).pack(anchor="w")
        self.mat_a_txt = tk.Text(f, height=4, width=40, bg=COLORS["surface_alt"], fg="#ffffff", font=("Consolas", 10))
        self.mat_a_txt.pack(anchor="w", pady=(2, 8))
        self.mat_a_txt.insert(tk.END, "1 2\n3 4")

        tk.Label(f, text="Matriz B (para operações binárias de soma, subtração e multiplicação):", bg=COLORS["surface"], fg=COLORS["text_muted"]).pack(anchor="w")
        self.mat_b_txt = tk.Text(f, height=4, width=40, bg=COLORS["surface_alt"], fg="#ffffff", font=("Consolas", 10))
        self.mat_b_txt.pack(anchor="w", pady=(2, 8))
        self.mat_b_txt.insert(tk.END, "5 6\n7 8")

        b_row = tk.Frame(f, bg=COLORS["surface"])
        b_row.pack(fill=tk.X, pady=6)

        tk.Button(b_row, text="A + B", bg=COLORS["surface_alt"], fg="#ffffff", relief=tk.FLAT, padx=10, command=lambda: self._exec_mat_op("add")).pack(side=tk.LEFT, padx=3)
        tk.Button(b_row, text="A - B", bg=COLORS["surface_alt"], fg="#ffffff", relief=tk.FLAT, padx=10, command=lambda: self._exec_mat_op("sub")).pack(side=tk.LEFT, padx=3)
        tk.Button(b_row, text="A × B", bg=COLORS["accent_primary"], fg="#ffffff", relief=tk.FLAT, padx=10, command=lambda: self._exec_mat_op("mul")).pack(side=tk.LEFT, padx=3)
        tk.Button(b_row, text="Transposta (Aᵀ)", bg=COLORS["surface_alt"], fg="#ffffff", relief=tk.FLAT, padx=10, command=lambda: self._exec_mat_op("trans")).pack(side=tk.LEFT, padx=3)
        tk.Button(b_row, text="Determinante (det A)", bg=COLORS["accent_hover"], fg="#ffffff", relief=tk.FLAT, padx=10, command=lambda: self._exec_mat_op("det")).pack(side=tk.LEFT, padx=3)

        self.mat_out_txt = tk.Text(f, height=6, bg=COLORS["bg_dark"], fg=COLORS["text_primary"], font=("Consolas", 11), relief=tk.FLAT)
        self.mat_out_txt.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

    def _parse_matrix(self, widget: tk.Text):
        raw = widget.get("1.0", tk.END).strip().splitlines()
        mat = []
        for line in raw:
            parts = line.strip().split()
            if parts:
                mat.append([float(x.replace(',', '.')) for x in parts])
        return mat

    def _format_matrix(self, mat):
        return "\n".join(["  [ " + "  ".join([f"{val:>8.4g}" for val in row]) + " ]" for row in mat])

    def _exec_mat_op(self, op: str):
        try:
            a = self._parse_matrix(self.mat_a_txt)
            if op == "det":
                d = MatrixEngine.determinant(a)
                self.mat_out_txt.delete("1.0", tk.END)
                self.mat_out_txt.insert(tk.END, f"Determinante de A: det(A) = {d}")
                return
            if op == "trans":
                t = MatrixEngine.transpose(a)
                self.mat_out_txt.delete("1.0", tk.END)
                self.mat_out_txt.insert(tk.END, f"Matriz Transposta Aᵀ:\n{self._format_matrix(t)}")
                return

            b = self._parse_matrix(self.mat_b_txt)
            if op == "add":
                res = MatrixEngine.add(a, b)
                lbl = "Soma A + B"
            elif op == "sub":
                res = MatrixEngine.subtract(a, b)
                lbl = "Subtração A - B"
            else:
                res = MatrixEngine.multiply(a, b)
                lbl = "Multiplicação A × B"

            self.mat_out_txt.delete("1.0", tk.END)
            self.mat_out_txt.insert(tk.END, f"{lbl}:\n{self._format_matrix(res)}")
        except Exception as e:
            messagebox.showerror("Erro Matricial", str(e))

    # =========================================================================
    # 9. ABA DATA E HORA
    # =========================================================================

    def _build_datetime_tab(self):
        f = self.tab_datetime
        tk.Label(f, text="Cálculos de Calendário, Idade e Dias Úteis", font=("Segoe UI", 14, "bold"), fg=COLORS["accent_light"], bg=COLORS["surface"]).pack(anchor="w", pady=(0, 15))

        box = tk.LabelFrame(f, text="Diferença Entre Duas Datas", bg=COLORS["surface"], fg=COLORS["text_primary"], padx=10, pady=10)
        box.pack(fill=tk.X, pady=(0, 15))

        r = tk.Frame(box, bg=COLORS["surface"])
        r.pack(fill=tk.X, pady=4)

        tk.Label(r, text="Data Inicial (DD/MM/AAAA):", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.dt_d1 = tk.Entry(r, width=12, bg=COLORS["surface_alt"], fg="#ffffff"); self.dt_d1.pack(side=tk.LEFT, padx=4); self.dt_d1.insert(0, "01/01/2024")

        tk.Label(r, text="Data Final (DD/MM/AAAA):", bg=COLORS["surface"]).pack(side=tk.LEFT, padx=(10, 0))
        self.dt_d2 = tk.Entry(r, width=12, bg=COLORS["surface_alt"], fg="#ffffff"); self.dt_d2.pack(side=tk.LEFT, padx=4); self.dt_d2.insert(0, "31/12/2024")

        tk.Button(r, text="Calcular Intervalo", bg=COLORS["accent_primary"], fg="#ffffff", relief=tk.FLAT, command=self._calc_dates).pack(side=tk.LEFT, padx=12)

        self.dt_res_lbl = tk.Label(box, text="Resumo: -", font=("Consolas", 11, "bold"), fg=COLORS["accent_light"], bg=COLORS["surface"])
        self.dt_res_lbl.pack(anchor="w", pady=(8, 0))

    def _calc_dates(self):
        try:
            d1 = self.dt_d1.get()
            d2 = self.dt_d2.get()
            diff = DateTimeCalculator.date_difference(d1, d2)
            txt = f"{diff['resumo']}\nDias Úteis (Seg-Sex): {diff['dias_uteis']} dias"
            self.dt_res_lbl.config(text=txt)
        except Exception as e:
            messagebox.showerror("Erro Data/Hora", str(e))

    # =========================================================================
    # 10. ABA HISTÓRICO E PERSISTÊNCIA
    # =========================================================================

    def _build_history_tab(self):
        f = self.tab_history
        tk.Label(f, text="Histórico Local Persistente (JSON)", font=("Segoe UI", 14, "bold"), fg=COLORS["accent_light"], bg=COLORS["surface"]).pack(anchor="w", pady=(0, 10))

        top_ctrl = tk.Frame(f, bg=COLORS["surface"])
        top_ctrl.pack(fill=tk.X, pady=(0, 10))

        tk.Label(top_ctrl, text="Buscar no Histórico:", bg=COLORS["surface"]).pack(side=tk.LEFT)
        self.hist_search_entry = tk.Entry(top_ctrl, width=20, bg=COLORS["surface_alt"], fg="#ffffff")
        self.hist_search_entry.pack(side=tk.LEFT, padx=6)
        self.hist_search_entry.bind("<KeyRelease>", lambda e: self._refresh_history_list())

        tk.Button(top_ctrl, text="Atualizar", bg=COLORS["surface_alt"], fg=COLORS["text_primary"], relief=tk.FLAT, command=self._refresh_history_list).pack(side=tk.LEFT, padx=4)
        tk.Button(top_ctrl, text="Exportar CSV", bg=COLORS["accent_primary"], fg="#ffffff", relief=tk.FLAT, command=self._export_csv).pack(side=tk.LEFT, padx=4)
        tk.Button(top_ctrl, text="Exportar JSON", bg=COLORS["accent_hover"], fg="#ffffff", relief=tk.FLAT, command=self._export_json).pack(side=tk.LEFT, padx=4)
        tk.Button(top_ctrl, text="Limpar Tudo", bg=COLORS["danger"], fg="#ffffff", relief=tk.FLAT, command=self._clear_all_history).pack(side=tk.RIGHT)

        # Tabela Treeview de Histórico
        columns = ("id", "timestamp", "categoria", "expressao", "resultado")
        self.hist_tree = ttk.Treeview(f, columns=columns, show="headings", height=14)
        self.hist_tree.heading("id", text="#")
        self.hist_tree.heading("timestamp", text="Data/Hora")
        self.hist_tree.heading("categoria", text="Categoria")
        self.hist_tree.heading("expressao", text="Expressão")
        self.hist_tree.heading("resultado", text="Resultado")

        self.hist_tree.column("id", width=40, anchor="center")
        self.hist_tree.column("timestamp", width=140, anchor="center")
        self.hist_tree.column("categoria", width=100, anchor="center")
        self.hist_tree.column("expressao", width=260)
        self.hist_tree.column("resultado", width=180)

        self.hist_tree.pack(fill=tk.BOTH, expand=True)
        self._refresh_history_list()

    def _refresh_history_list(self):
        query = self.hist_search_entry.get()
        records = self.history_mgr.search(query)
        for row in self.hist_tree.get_children():
            self.hist_tree.delete(row)
        for r in records:
            self.hist_tree.insert("", tk.END, values=(
                r.get("id"),
                r.get("timestamp"),
                r.get("categoria"),
                r.get("expressao"),
                r.get("resultado"),
            ))

    def _export_csv(self):
        fp = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if fp:
            success = self.history_mgr.export_csv(fp)
            if success:
                messagebox.showinfo("Exportado", f"Histórico exportado com sucesso para:\n{fp}")
            else:
                messagebox.showerror("Erro", "Falha ao gravar arquivo CSV.")

    def _export_json(self):
        fp = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if fp:
            success = self.history_mgr.export_json(fp)
            if success:
                messagebox.showinfo("Exportado", f"Histórico exportado com sucesso para:\n{fp}")
            else:
                messagebox.showerror("Erro", "Falha ao gravar arquivo JSON.")

    def _clear_all_history(self):
        confirm = messagebox.askyesno("Confirmação", "Deseja realmente limpar todo o histórico persistente?")
        if confirm:
            self.history_mgr.clear_all()
            self._refresh_history_list()

    def _bind_keyboard_shortcuts(self):
        self.root.bind("<Return>", lambda e: self._evaluate_calc())
        self.root.bind("<KP_Enter>", lambda e: self._evaluate_calc())
        self.root.bind("<Escape>", lambda e: self._on_calc_btn_press("C"))
