"""
Interpretador Matemático Seguro
Implementa tokenização explícita, análise sintática e avaliação controlada.
PROIBIDO USO DE eval() OU exec().
"""

import math
import re
from typing import List, Dict, Callable, Union, Optional, Any
from app.validators import ValidationError, MathDomainError


class TokenType:
    NUMBER = "NUMBER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    INT_DIV = "INT_DIV"
    MOD = "MOD"
    POW = "POW"
    FACTORIAL = "FACTORIAL"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    COMMA = "COMMA"
    IDENT = "IDENT"
    EOF = "EOF"


class Token:
    def __init__(self, type_: str, value: Any = None, pos: int = 0):
        self.type = type_
        self.value = value
        self.pos = pos

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, pos={self.pos})"


class SafeExpressionParser:
    """
    Parser recursivo descendente seguro para expressões matemáticas.
    Totalmente isolado do interpretador Python padrão.
    """

    MAX_EXPRESSION_LENGTH = 500
    MAX_EXPONENT = 10000

    def __init__(self, angle_mode: str = "deg"):
        # angle_mode: 'deg' ou 'rad'
        self.angle_mode = angle_mode.lower()

        # Constantes matemáticas autorizadas
        self.constants: Dict[str, float] = {
            "pi": math.pi,
            "π": math.pi,
            "e": math.e,
            "tau": math.tau,
            "phi": (1 + math.sqrt(5)) / 2,
        }

        # Funções matemáticas autorizadas
        self.functions: Dict[str, Callable] = {
            "sin": self._sin,
            "cos": self._cos,
            "tan": self._tan,
            "asin": self._asin,
            "acos": self._acos,
            "atan": self._atan,
            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,
            "sqrt": self._sqrt,
            "cbrt": lambda x: math.copysign(abs(x) ** (1.0 / 3.0), x),
            "log": self._log10,  # log comum (base 10)
            "log10": self._log10,
            "log2": self._log2,
            "ln": self._ln,
            "exp": self._exp,
            "abs": abs,
            "floor": math.floor,
            "ceil": math.ceil,
            "round": round,
            "fact": self._fact,
            "rad": math.radians,
            "deg": math.degrees,
        }

    # Wrapper trigonométrico respeitando angle_mode
    def _sin(self, x: float) -> float:
        rad = math.radians(x) if self.angle_mode == "deg" else x
        val = math.sin(rad)
        return 0.0 if abs(val) < 1e-15 else val

    def _cos(self, x: float) -> float:
        rad = math.radians(x) if self.angle_mode == "deg" else x
        val = math.cos(rad)
        return 0.0 if abs(val) < 1e-15 else val

    def _tan(self, x: float) -> float:
        rad = math.radians(x) if self.angle_mode == "deg" else x
        cos_val = math.cos(rad)
        if abs(cos_val) < 1e-15:
            raise MathDomainError("Tangente indefinida (divisão por zero / cosseno nulo).")
        val = math.tan(rad)
        return 0.0 if abs(val) < 1e-15 else val

    def _asin(self, x: float) -> float:
        if x < -1.0 or x > 1.0:
            raise MathDomainError("Arco-seno indefinido para valores fora de [-1, 1].")
        res = math.asin(x)
        return math.degrees(res) if self.angle_mode == "deg" else res

    def _acos(self, x: float) -> float:
        if x < -1.0 or x > 1.0:
            raise MathDomainError("Arco-cosseno indefinido para valores fora de [-1, 1].")
        res = math.acos(x)
        return math.degrees(res) if self.angle_mode == "deg" else res

    def _atan(self, x: float) -> float:
        res = math.atan(x)
        return math.degrees(res) if self.angle_mode == "deg" else res

    def _sqrt(self, x: float) -> float:
        if x < 0:
            raise MathDomainError("Raiz quadrada de número negativo não permitida no domínio real.")
        return math.sqrt(x)

    def _log10(self, x: float) -> float:
        if x <= 0:
            raise MathDomainError("Logaritmo na base 10 indefinido para valores menores ou iguais a zero.")
        return math.log10(x)

    def _log2(self, x: float) -> float:
        if x <= 0:
            raise MathDomainError("Logaritmo na base 2 indefinido para valores menores ou iguais a zero.")
        return math.log2(x)

    def _ln(self, x: float) -> float:
        if x <= 0:
            raise MathDomainError("Logaritmo natural (ln) indefinido para valores menores ou iguais a zero.")
        return math.log(x)

    def _exp(self, x: float) -> float:
        if x > 700:
            raise MathDomainError("Exponencial muito grande; risco de estouro de ponto flutuante.")
        return math.exp(x)

    def _fact(self, x: float) -> int:
        if not float(x).is_integer():
            raise MathDomainError("Fatorial só é definido para inteiros.")
        val = int(x)
        if val < 0:
            raise MathDomainError("Fatorial indefinido para números negativos.")
        if val > 170:
            raise MathDomainError("Fatorial de números acima de 170 excede limite de ponto flutuante IEEE-754.")
        return math.factorial(val)

    def tokenize(self, expression: str) -> List[Token]:
        """Converte a string da expressão em uma lista de tokens seguros."""
        if not expression or not expression.strip():
            raise ValidationError("A expressão informada está vazia.")

        expr = expression.strip()
        if len(expr) > self.MAX_EXPRESSION_LENGTH:
            raise ValidationError(
                f"Expressão excede o limite máximo de {self.MAX_EXPRESSION_LENGTH} caracteres."
            )

        # Substitui possíveis vírgulas decimais quando não usadas como separador de argumentos
        # Ex: 3,5 + 2 -> 3.5 + 2
        # Mantém vírgulas dentro de chamadas como log(a, b)
        tokens: List[Token] = []
        i = 0
        n = len(expr)

        while i < n:
            ch = expr[i]

            if ch.isspace():
                i += 1
                continue

            # Dígrafos ou operadores de dois caracteres
            if ch == '/' and i + 1 < n and expr[i + 1] == '/':
                tokens.append(Token(TokenType.INT_DIV, "//", i))
                i += 2
                continue

            if ch == '*' and i + 1 < n and expr[i + 1] == '*':
                tokens.append(Token(TokenType.POW, "**", i))
                i += 2
                continue

            # Operadores unitários simples
            if ch == '+':
                tokens.append(Token(TokenType.PLUS, "+", i))
                i += 1
            elif ch == '-':
                tokens.append(Token(TokenType.MINUS, "-", i))
                i += 1
            elif ch == '*' or ch == '×':
                tokens.append(Token(TokenType.MUL, "*", i))
                i += 1
            elif ch == '/' or ch == '÷':
                tokens.append(Token(TokenType.DIV, "/", i))
                i += 1
            elif ch == '%':
                tokens.append(Token(TokenType.MOD, "%", i))
                i += 1
            elif ch == '^':
                tokens.append(Token(TokenType.POW, "^", i))
                i += 1
            elif ch == '!':
                tokens.append(Token(TokenType.FACTORIAL, "!", i))
                i += 1
            elif ch == '(':
                tokens.append(Token(TokenType.LPAREN, "(", i))
                i += 1
            elif ch == ')':
                tokens.append(Token(TokenType.RPAREN, ")", i))
                i += 1
            elif ch == ';' or ch == ',':
                # Verifica se é vírgula decimal entre dígitos: ex '3,5'
                if ch == ',' and i > 0 and expr[i - 1].isdigit() and i + 1 < n and expr[i + 1].isdigit():
                    # Trata como separador decimal fundindo com o número anterior se aplicável
                    # Para tokenização limpa, lidaremos abaixo no leitor de números
                    tokens.append(Token(TokenType.COMMA, ",", i))
                else:
                    tokens.append(Token(TokenType.COMMA, ",", i))
                i += 1
            elif ch.isdigit() or (ch == '.' and i + 1 < n and expr[i + 1].isdigit()):
                start_pos = i
                dot_count = 0
                num_str = ""
                while i < n and (expr[i].isdigit() or expr[i] == '.'):
                    if expr[i] == '.':
                        dot_count += 1
                        if dot_count > 1:
                            raise ValidationError(f"Número inválido com múltiplos pontos na posição {i}.")
                    num_str += expr[i]
                    i += 1

                # Suporte a notação científica e/E
                if i < n and (expr[i] == 'e' or expr[i] == 'E'):
                    # Confirma se é notação científica e não início de identificador 'exp'
                    if i + 1 < n and (expr[i + 1].isdigit() or expr[i + 1] in '+-'):
                        num_str += expr[i]
                        i += 1
                        if i < n and expr[i] in '+-':
                            num_str += expr[i]
                            i += 1
                        while i < n and expr[i].isdigit():
                            num_str += expr[i]
                            i += 1

                try:
                    num_val = float(num_str) if '.' in num_str or 'e' in num_str.lower() else int(num_str)
                    tokens.append(Token(TokenType.NUMBER, num_val, start_pos))
                except ValueError as err:
                    raise ValidationError(f"Número malformado '{num_str}' na posição {start_pos}.") from err

            elif ch.isalpha() or ch == 'π':
                start_pos = i
                ident = ""
                while i < n and (expr[i].isalnum() or expr[i] == '_' or expr[i] == 'π'):
                    ident += expr[i]
                    i += 1

                ident_lower = ident.lower()
                # Validação estrita: somente funções ou constantes permitidas
                if ident_lower in self.constants or ident_lower in self.functions:
                    tokens.append(Token(TokenType.IDENT, ident_lower, start_pos))
                else:
                    raise ValidationError(
                        f"Identificador não reconhecido ou não autorizado: '{ident}'. "
                        f"Comandos Python e chamadas externas são proibidos."
                    )
            else:
                raise ValidationError(f"Caractere não permitido '{ch}' na posição {i}.")

        tokens.append(Token(TokenType.EOF, None, n))
        return tokens

    def evaluate(self, expression: str) -> Union[int, float]:
        """Analisa sintaticamente e calcula o resultado numérico da expressão."""
        # Pré-processa vírgula decimal entre dígitos se não for delimitador de função
        # Ex: "12,5 + 3,2" -> "12.5 + 3.2"
        sanitized = re.sub(r'(\d+),(\d+)', r'\1.\2', expression)
        tokens = self.tokenize(sanitized)
        pos = 0

        def current() -> Token:
            nonlocal pos
            return tokens[pos]

        def peek(offset: int = 1) -> Token:
            nonlocal pos
            idx = pos + offset
            return tokens[idx] if idx < len(tokens) else tokens[-1]

        def advance() -> Token:
            nonlocal pos
            tok = tokens[pos]
            if tok.type != TokenType.EOF:
                pos += 1
            return tok

        def expect(expected_type: str, err_msg: str = "") -> Token:
            tok = current()
            if tok.type != expected_type:
                msg = err_msg or f"Esperado '{expected_type}', mas encontrado '{tok.type}' na posição {tok.pos}."
                raise ValidationError(msg)
            return advance()

        # Gramática com Precedência Operacional Clássica:
        # expr := term ((PLUS | MINUS) term)*
        # term := factor ((MUL | DIV | INT_DIV | MOD) factor)*
        # factor := power
        # power := unary (POW power)?  (associativo à direita)
        # unary := (PLUS | MINUS) unary | postfix
        # postfix := primary FACTORIAL*
        # primary := NUMBER | IDENT ( '(' args? ')' )? | '(' expr ')'

        def parse_expr() -> Union[int, float]:
            result = parse_term()
            while current().type in (TokenType.PLUS, TokenType.MINUS):
                op = advance()
                right = parse_term()
                if op.type == TokenType.PLUS:
                    result = result + right
                else:
                    result = result - right
            return result

        def parse_term() -> Union[int, float]:
            result = parse_power()
            while current().type in (TokenType.MUL, TokenType.DIV, TokenType.INT_DIV, TokenType.MOD):
                op = advance()
                right = parse_power()
                if op.type == TokenType.MUL:
                    result = result * right
                elif op.type == TokenType.DIV:
                    if right == 0:
                        raise MathDomainError("Divisão por zero não é permitida.")
                    result = result / right
                elif op.type == TokenType.INT_DIV:
                    if right == 0:
                        raise MathDomainError("Divisão inteira por zero não é permitida.")
                    result = result // right
                elif op.type == TokenType.MOD:
                    if right == 0:
                        raise MathDomainError("Operação de módulo por zero não é permitida.")
                    result = result % right
            return result

        def parse_power() -> Union[int, float]:
            left = parse_unary()
            if current().type == TokenType.POW:
                advance()
                right = parse_power()  # Associatividade à direita
                if abs(right) > self.MAX_EXPONENT:
                    raise MathDomainError(f"Expoente {right} excede o limite máximo seguro de {self.MAX_EXPONENT}.")
                try:
                    # Trata raiz fracionária de número negativo
                    if left < 0 and not float(right).is_integer():
                        raise MathDomainError("Potenciação de base negativa com expoente não-inteiro resulta em número complexo.")
                    res = left ** right
                    return res
                except OverflowError as err:
                    raise MathDomainError("Estouro de capacidade numérica na potenciação.") from err
            return left

        def parse_unary() -> Union[int, float]:
            if current().type == TokenType.PLUS:
                advance()
                return parse_unary()
            if current().type == TokenType.MINUS:
                advance()
                return -parse_unary()
            return parse_postfix()

        def parse_postfix() -> Union[int, float]:
            val = parse_primary()
            while current().type == TokenType.FACTORIAL:
                advance()
                val = self._fact(val)
            return val

        def parse_primary() -> Union[int, float]:
            tok = current()

            if tok.type == TokenType.NUMBER:
                advance()
                return tok.value

            if tok.type == TokenType.LPAREN:
                advance()
                val = parse_expr()
                expect(TokenType.RPAREN, "Parêntese de fechamento ')' ausente.")
                return val

            if tok.type == TokenType.IDENT:
                name = tok.value
                advance()

                # Verifica se é uma chamada de função (seguida por '(')
                if current().type == TokenType.LPAREN:
                    advance()
                    args = []
                    if current().type != TokenType.RPAREN:
                        args.append(parse_expr())
                        while current().type == TokenType.COMMA:
                            advance()
                            args.append(parse_expr())
                    expect(TokenType.RPAREN, f"Fechamento de parênteses esperado para a função '{name}'.")

                    if name not in self.functions:
                        raise ValidationError(f"Função '{name}' não encontrada ou não permitida.")

                    func = self.functions[name]
                    try:
                        return func(*args)
                    except TypeError as exc:
                        raise ValidationError(f"Número incorreto de argumentos para a função '{name}': {exc}.") from exc
                else:
                    # Constante matemática
                    if name in self.constants:
                        return self.constants[name]
                    # Se for função sem parênteses, erro claro
                    if name in self.functions:
                        raise ValidationError(f"Função '{name}' requer parênteses. Exemplo: {name}(valor).")
                    raise ValidationError(f"Identificador desconhecido '{name}'.")

            raise ValidationError(
                f"Sintaxe inesperada: encontrado '{tok.value or tok.type}' na posição {tok.pos}."
            )

        final_result = parse_expr()
        if current().type != TokenType.EOF:
            extra = current()
            raise ValidationError(
                f"Símbolo inesperado após término da expressão: '{extra.value or extra.type}' na posição {extra.pos}."
            )

        # Se for um float que representa inteiro exato (ex: 4.0), mantém legibilidade
        if isinstance(final_result, float) and final_result.is_integer() and abs(final_result) < 1e15:
            return int(final_result)
        return final_result
