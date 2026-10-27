# 📔 Python Ultimate Calculator — Calculadora Multifuncional Avançada

Uma aplicação completa de cálculo científico, financeiro, estatístico, algébrico e geométrico desenvolvida em **Python 3.10+ / 3.12** com interface gráfica moderna em **Tkinter/ttk** e edição web interativa.

---

## 🚀 Visão Geral e Características

- **Segurança Rigorosa**: Interpretador matemático seguro baseado em árvore sintática (AST) e parser recursivo descendente com tokenização explícita. **Zero uso de `eval()` ou `exec()`**.
- **Alta Precisão Financeira**: Módulo financeiro com `Decimal` para evitar imprecisões de ponto flutuante e formatação no padrão brasileiro (`R$ 1.250,50`).
- **Aritmética Exata**: Preservação de frações exatas com a classe `Fraction`, MDC, MMC e fatoração prima.
- **Álgebra com Passo a Passo**: Resolução de equações de 1º e 2º grau (Bhaskara com discriminante $\Delta$, raízes reais e complexas), sistemas lineares 2x2 com identificação de SPD, SPI e SI.
- **Estatística e Probabilidade**: Média, mediana, moda, variâncias e desvios-padrão amostral e populacional, quartis, percentis e distribuições de frequência.
- **Conversores de Unidades**: 11 categorias de grandezas (distinguindo unidades decimais MB de binárias MiB).
- **Geometria 2D e 3D**: Áreas, perímetros, volumes, superfícies, Teorema de Pitágoras e distância euclidiana.
- **Álgebra Linear**: Matrizes e vetores (soma, subtração, produto matricial, escalar, determinante e norma).
- **Cálculo Temporal**: Contagem de dias úteis, diferença em anos/meses/dias e cálculo de idade.
- **Histórico Persistente**: Armazenamento local em JSON com busca, reuso de cálculos e exportação para CSV e JSON.
- **60 Testes Unitários Automatizados**: Cobertura determinística de todos os módulos com Python `unittest`.

---

## 📁 Estrutura do Projeto

```text
python-ultimate-calculator/
├── main.py                     # Ponto de entrada da aplicação
├── requirements.txt            # Dependências do projeto
├── README.md                   # Documentação completa
├── .gitignore                  # Arquivos ignorados pelo Git
├── metadata.json               # Metadados da aplicação
├── app/                        # Módulos centrais da aplicação
│   ├── __init__.py             # Inicialização do pacote
│   ├── interface.py            # Interface gráfica desktop em Tkinter/ttk
│   ├── calculator_engine.py    # Motor unificado de cálculo e memória
│   ├── expression_parser.py    # Parser matemático seguro sem eval()
│   ├── scientific.py           # Funções científicas, trigonométricas e logs
│   ├── fractions_math.py       # Aritmética de frações, MDC, MMC e primos
│   ├── algebra.py              # Equações 1º/2º grau e sistemas 2x2
│   ├── statistics_tools.py     # Análise descritiva e probabilidade
│   ├── finance.py              # Financiamento Price, juros e markup
│   ├── converters.py           # 11 categorias de conversão de unidades
│   ├── date_time.py            # Calendário, dias úteis e idade
│   ├── geometry.py             # Geometria 2D/3D e Pitágoras
│   ├── matrices.py             # Operações com matrizes e vetores
│   ├── history.py              # Histórico persistente e exportação CSV/JSON
│   ├── settings.py             # Preferências do usuário em JSON
│   └── validators.py           # Validações de limites e domínios matemáticos
├── tests/                      # Suíte de 60 testes unitários determinísticos
│   ├── __init__.py
│   ├── test_basic.py
│   ├── test_scientific.py
│   ├── test_expression_parser.py
│   ├── test_finance.py
│   ├── test_converters.py
│   ├── test_statistics.py
│   ├── test_algebra.py
│   ├── test_matrices.py
│   └── test_history.py
├── data/                       # Diretório para persistência local (JSON)
│   └── .gitkeep
└── src/                        # Edição Web interativa
    ├── public/                 # Versão web estática standalone
    │   ├── index.html
    │   ├── style.css
    │   └── script.js
    ├── App.tsx                 # Interface Web React de alta fidelidade
    └── main.tsx
```

---

## 🛠 Requisitos e Instalação

### Requisitos Mínimos
- Python 3.10 ou superior (testado e homologado em Python 3.10 e 3.12).
- Sistema Operacional: Windows, Linux ou macOS.

### Passo 1: Clonar ou Baixar o Repositório
```bash
git clone <url-do-repositorio>
cd python-ultimate-calculator
```

### Passo 2: Criar e Ativar o Ambiente Virtual

**No Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**No Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**No Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### Passo 3: Instalar as Dependências
```bash
pip install -r requirements.txt
```

---

## ▶️ Como Executar a Aplicação

### Interface Desktop (Tkinter)
Execute o arquivo principal:
```bash
python3 main.py
```
*(No Windows: `python main.py`)*

### Interface Web
Caso queira executar a interface web de pré-visualização:
```bash
npm install
npm run dev
```
Acesse `http://localhost:3000` no seu navegador.

---

## 🧪 Execução dos Testes Automatizados

A aplicação inclui uma suíte com **60 testes unitários automatizados determinísticos** cobrindo todos os módulos matemáticos e o interpretador seguro:

```bash
python3 -m unittest discover tests -v
```

### Resultados dos Testes
```text
test_linear_system_si (test_algebra.TestAlgebraSolver) ... ok
test_linear_system_spd (test_algebra.TestAlgebraSolver) ... ok
test_linear_system_spi (test_algebra.TestAlgebraSolver) ... ok
test_quadratic_complex_roots (test_algebra.TestAlgebraSolver) ... ok
test_quadratic_distinct_real_roots (test_algebra.TestAlgebraSolver) ... ok
test_quadratic_double_real_root (test_algebra.TestAlgebraSolver) ... ok
test_solve_linear (test_algebra.TestAlgebraSolver) ... ok
test_basic_evaluation (test_basic.TestCalculatorEngine) ... ok
test_inverse (test_basic.TestCalculatorEngine) ... ok
test_memory_operations (test_basic.TestCalculatorEngine) ... ok
test_percentage (test_basic.TestCalculatorEngine) ... ok
test_toggle_sign (test_basic.TestCalculatorEngine) ... ok
test_absolute_zero_validation (test_converters.TestUnitConverter) ... ok
test_digital_data_mb_vs_mib (test_converters.TestUnitConverter) ... ok
test_length_conversion (test_converters.TestUnitConverter) ... ok
test_temperature_conversion (test_converters.TestUnitConverter) ... ok
test_time_conversion (test_converters.TestUnitConverter) ... ok
test_authorized_constants (test_expression_parser.TestSafeExpressionParser) ... ok
test_authorized_functions (test_expression_parser.TestSafeExpressionParser) ... ok
test_basic_arithmetic (test_expression_parser.TestSafeExpressionParser) ... ok
test_decimal_comma_and_dot (test_expression_parser.TestSafeExpressionParser) ... ok
test_division_by_zero (test_expression_parser.TestSafeExpressionParser) ... ok
test_factorial (test_expression_parser.TestSafeExpressionParser) ... ok
test_log_zero_or_negative (test_expression_parser.TestSafeExpressionParser) ... ok
test_negative_square_root (test_expression_parser.TestSafeExpressionParser) ... ok
test_operator_precedence (test_expression_parser.TestSafeExpressionParser) ... ok
test_security_rejection_of_python_code (test_expression_parser.TestSafeExpressionParser) ... ok
test_syntax_errors (test_expression_parser.TestSafeExpressionParser) ... ok
test_unary_signs (test_expression_parser.TestSafeExpressionParser) ... ok
test_brl_formatting (test_finance.TestFinanceEngine) ... ok
test_compound_interest (test_finance.TestFinanceEngine) ... ok
test_invalid_margin_over_100 (test_finance.TestFinanceEngine) ... ok
test_margin_and_markup (test_finance.TestFinanceEngine) ... ok
test_price_financing (test_finance.TestFinanceEngine) ... ok
test_price_from_desired_margin (test_finance.TestFinanceEngine) ... ok
test_rate_conversion (test_finance.TestFinanceEngine) ... ok
test_simple_interest (test_finance.TestFinanceEngine) ... ok
test_add_and_retrieve (test_history.TestHistoryManager) ... ok
test_delete_and_clear (test_history.TestHistoryManager) ... ok
test_export_csv_and_json (test_history.TestHistoryManager) ... ok
test_search (test_history.TestHistoryManager) ... ok
test_add (test_matrices.TestMatrixEngine) ... ok
test_determinant_2x2 (test_matrices.TestMatrixEngine) ... ok
test_determinant_3x3 (test_matrices.TestMatrixEngine) ... ok
test_incompatible_dimensions (test_matrices.TestMatrixEngine) ... ok
test_multiply (test_matrices.TestMatrixEngine) ... ok
test_subtract (test_matrices.TestMatrixEngine) ... ok
test_transpose (test_matrices.TestMatrixEngine) ... ok
test_vector_dot_product (test_matrices.TestMatrixEngine) ... ok
test_vector_norm (test_matrices.TestMatrixEngine) ... ok
test_combinatorics (test_scientific.TestScientificCalculator) ... ok
test_inverse_trigonometry (test_scientific.TestScientificCalculator) ... ok
test_logarithms (test_scientific.TestScientificCalculator) ... ok
test_nth_root (test_scientific.TestScientificCalculator) ... ok
test_trigonometry_degrees (test_scientific.TestScientificCalculator) ... ok
test_trigonometry_radians (test_scientific.TestScientificCalculator) ... ok
test_descriptive_analysis (test_statistics.TestStatisticsEngine) ... ok
test_parse_series (test_statistics.TestStatisticsEngine) ... ok
test_probability (test_statistics.TestStatisticsEngine) ... ok
test_weighted_mean (test_statistics.TestStatisticsEngine) ... ok
----------------------------------------------------------------------
Ran 60 tests in 0.012s - OK
```

---

## 📦 Como Gerar Executável para Windows (.exe)

Para empacotar a aplicação em um executável autônomo para Windows utilizando o **PyInstaller**:

1. Instale o PyInstaller no seu ambiente:
   ```bash
   pip install pyinstaller
   ```

2. Execute o comando de compilação:
   ```bash
   pyinstaller --noconsole --onefile --name "PythonUltimateCalculator" --icon=app_icon.ico main.py
   ```
   *(Omita `--icon=app_icon.ico` caso não possua um arquivo de ícone).*

3. O executável pronto será gerado no diretório `dist/PythonUltimateCalculator.exe`.

---

## 🔒 Segurança do Interpretador Matemático

O módulo `app/expression_parser.py` foi projetado especificamente para eliminar o risco de execução de código arbitrário:
- Proíbe rigorosamente `eval()` e `exec()`.
- Divide a entrada em tokens explícitos (`NUMBER`, `PLUS`, `MINUS`, `IDENT`, etc.).
- Valida a gramática de precedência por descida recursiva.
- Aceita exclusivamente funções autorizadas (`sin`, `cos`, `tan`, `sqrt`, `log10`, `ln`, `abs`, etc.) e constantes matemáticas (`pi`, `e`, `tau`, `phi`).
- Rejeita qualquer comando Python (`import`, `open`, `os`, `sys`, `__globals__`, etc.) gerando erro imediato em português.

---

## 📄 Licença

Desenvolvido sob a licença MIT. Livre para uso acadêmico, educacional e comercial.
