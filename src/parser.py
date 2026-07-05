"""
parser.py — Tokenizer + recursive descent parser.

Converts a math expression string into an AST built from ast_nodes.py.
Depends on: ast_nodes.py

Grammar (standard precedence-climbing style, lowest to highest precedence):

    expression := term (('+' | '-') term)*
    term       := factor (('*' | '/') factor)*
    factor     := power
    power      := unary ('^' factor)?          # right-associative
    unary      := '-' unary | primary
    primary    := NUMBER
                | SYMBOL
                | SYMBOL '(' expression ')'     # function call: sin(x), ln(x)
                | '(' expression ')'

Note the right-recursion in `power`: factor on the right side of '^' lets
x^y^z parse as x^(y^z), matching standard math convention.
"""

from __future__ import annotations
from typing import List
from .ast_nodes import Node, Number, Symbol, BinaryOp, UnaryOp

KNOWN_FUNCTIONS = {'sin', 'cos', 'tan', 'ln', 'exp', 'sqrt'}


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

class Token:
    """
    A single lexical token.

    Pseudocode:
        store `type` (str: one of 'NUMBER', 'SYMBOL', 'OP', 'LPAREN', 'RPAREN')
        store `value` (str or float, the raw text / parsed number)

    __repr__: f"Token({self.type!r}, {self.value!r})"
    """

    def __init__(self, type_: str, value):
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError


def tokenize(expression: str) -> List[Token]:
    """
    Convert a raw expression string into a list of Tokens.

    Pseudocode:
        i = 0
        tokens = []
        while i < len(expression):
            char = expression[i]

            if char is whitespace:
                i += 1
                continue

            if char is a digit or '.':
                # consume a full number (handle multi-digit and decimals)
                # e.g. "3.14" should become one NUMBER token, not four
                start = i
                while i < len(expression) and (digit or '.'):
                    i += 1
                tokens.append(Token('NUMBER', float(expression[start:i])))
                continue

            if char is a letter:
                # consume a full identifier (symbol name or function name)
                start = i
                while i < len(expression) and (letter or digit):
                    i += 1
                tokens.append(Token('SYMBOL', expression[start:i]))
                continue

            if char in '+-*/^':
                tokens.append(Token('OP', char))
                i += 1
                continue

            if char == '(':
                tokens.append(Token('LPAREN', char))
                i += 1
                continue

            if char == ')':
                tokens.append(Token('RPAREN', char))
                i += 1
                continue

            raise ValueError(f"Unexpected character: {char!r} at position {i}")

        return tokens

    Edge cases to handle deliberately (don't just discover these via test
    failures — think about them before you type):
      - negative numbers vs subtraction: tokenize '-' as an OP always;
        distinguishing unary minus from binary minus is the PARSER's job,
        not the tokenizer's
      - multi-character symbols, e.g. "theta", "sin" — must not be split
        into single-char tokens
      - no space between tokens, e.g. "2x" or "2*x" — decide now whether
        implicit multiplication is in scope (recommended: NOT in scope for
        this scaffold; require explicit '*'). Document your choice in a
        comment once you implement this.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

class Parser:
    """
    Recursive descent parser. Holds a token list and a position cursor.

    Pseudocode for structure:
        __init__(self, tokens: List[Token]):
            store tokens
            store pos = 0

        _current(self) -> Token | None:
            return self.tokens[self.pos] if in bounds else None

        _advance(self) -> Token:
            token = self._current()
            self.pos += 1
            return token

        _expect(self, type_: str) -> Token:
            # consume current token if it matches type_, else raise
            # SyntaxError with a useful message (include what was expected
            # vs what was found)
    """

    def __init__(self, tokens: List[Token]):
        raise NotImplementedError

    def parse(self) -> Node:
        """
        Entry point. Parse the full token stream into a single AST.
        Must raise SyntaxError if tokens remain after parsing one
        expression (e.g. "2 + 3 )" has a dangling ')').

        Pseudocode:
            tree = self._parse_expression()
            if self._current() is not None:
                raise SyntaxError(f"Unexpected token: {self._current()}")
            return tree
        """
        raise NotImplementedError

    def _parse_expression(self) -> Node:
        """
        expression := term (('+' | '-') term)*

        Pseudocode:
            left = self._parse_term()
            while self._current() is an OP token with value '+' or '-':
                op = self._advance().value
                right = self._parse_term()
                left = BinaryOp(op, left, right)
            return left
        """
        raise NotImplementedError

    def _parse_term(self) -> Node:
        """
        term := factor (('*' | '/') factor)*
        Same shape as _parse_expression but one precedence level up and
        calling _parse_factor instead of _parse_term.
        """
        raise NotImplementedError

    def _parse_factor(self) -> Node:
        """
        factor := power
        A thin pass-through in this grammar — kept separate in case you
        want to add more precedence levels later without restructuring.
        """
        raise NotImplementedError

    def _parse_power(self) -> Node:
        """
        power := unary ('^' factor)?

        IMPORTANT: this is right-recursive (calls _parse_factor on the
        right side, not _parse_power), which is what makes '^' right-
        associative: x^y^z parses as x^(y^z).

        Pseudocode:
            base = self._parse_unary()
            if self._current() is an OP token with value '^':
                self._advance()
                exponent = self._parse_factor()   # NOT _parse_power — re-enter
                                                    # from a lower level so the
                                                    # whole right side is consumed
                                                    # as one unit, achieving
                                                    # right-associativity
                return BinaryOp('^', base, exponent)
            return base
        """
        raise NotImplementedError

    def _parse_unary(self) -> Node:
        """
        unary := '-' unary | primary

        Pseudocode:
            if self._current() is an OP token with value '-':
                self._advance()
                operand = self._parse_unary()   # recursive: handles "--x"
                return UnaryOp('-', operand)
            return self._parse_primary()
        """
        raise NotImplementedError

    def _parse_primary(self) -> Node:
        """
        primary := NUMBER
                 | SYMBOL
                 | SYMBOL '(' expression ')'
                 | '(' expression ')'

        Pseudocode:
            token = self._current()

            if token is None:
                raise SyntaxError("Unexpected end of input")

            if token.type == 'NUMBER':
                self._advance()
                return Number(token.value)

            if token.type == 'SYMBOL':
                self._advance()
                if self._current() is an LPAREN:
                    # function call: sin(x), ln(x), etc.
                    self._expect('LPAREN')
                    inner = self._parse_expression()
                    self._expect('RPAREN')
                    return UnaryOp(token.value, inner)
                else:
                    return Symbol(token.value)

            if token.type == 'LPAREN':
                self._expect('LPAREN')
                inner = self._parse_expression()
                self._expect('RPAREN')
                return inner

            raise SyntaxError(f"Unexpected token: {token}")
        """
        raise NotImplementedError


def parse(expression: str) -> Node:
    """
    Convenience wrapper: tokenize + parse in one call.

    Pseudocode:
        tokens = tokenize(expression)
        return Parser(tokens).parse()
    """
    raise NotImplementedError
