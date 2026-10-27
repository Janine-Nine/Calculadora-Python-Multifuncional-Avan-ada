#!/usr/bin/env python3
"""
Ponto de Entrada Principal (Main Entry Point)
Python Ultimate Calculator — Calculadora Multifuncional Avançada
Inicia a aplicação desktop em Tkinter ou modo console/diagnóstico em ambientes headless.
"""

import os
import sys
import tkinter as tk
from app.interface import UltimateCalculatorGUI


def main():
    print("Iniciando Python Ultimate Calculator...")
    try:
        root = tk.Tk()
        app = UltimateCalculatorGUI(root)
        root.mainloop()
    except tk.TclError as err:
        print(f"\n[AVISO] Interface gráfica desktop requer display gráfico X11/Wayland: {err}")
        print("Para executar a suíte completa de testes automatizados determinísticos:")
        print("  python3 -m unittest discover tests\n")
        print("Em ambiente web, utilize a interface gráfica completa no navegador!")


if __name__ == "__main__":
    main()
