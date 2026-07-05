import unittest
from src.ast_nodes import Number, Symbol, BinaryOp, UnaryOp
from src.parser import tokenize, parse, Parser, Token


class TestTokenizer(unittest.TestCase):
    def test_single_number(self):
        tokens = tokenize("5")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].type, 'NUMBER')
        self.assertEqual(tokens[0].value, 5.0)

    def test_decimal_number(self):
        tokens = tokenize("3.14")
        self.assertEqual(tokens[0].value, 3.14)

    def test_single_symbol(self):
        tokens = tokenize("x")
        self.assertEqual(tokens[0].type, 'SYMBOL')
        self.assertEqual(tokens[0].value, "x")

    def test_multichar_symbol(self):
        tokens = tokenize("theta")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].value, "theta")

    def test_operators(self):
        tokens = tokenize("+-*/^")
        self.assertEqual([t.value for t in tokens], ['+', '-', '*', '/', '^'])

    def test_parens(self):
        tokens = tokenize("()")
        self.assertEqual(tokens[0].type, 'LPAREN')
        self.assertEqual(tokens[1].type, 'RPAREN')

    def test_whitespace_ignored(self):
        tokens = tokenize("  x   +   1  ")
        self.assertEqual(len(tokens), 3)

    def test_full_expression(self):
        tokens = tokenize("x + 2 * y")
        types = [t.type for t in tokens]
        self.assertEqual(types, ['SYMBOL', 'OP', 'NUMBER', 'OP', 'SYMBOL'])

    def test_unknown_character_raises(self):
        with self.assertRaises(ValueError):
            tokenize("x @ y")


class TestParserBasics(unittest.TestCase):
    def test_single_number(self):
        self.assertEqual(parse("5"), Number(5))

    def test_single_symbol(self):
        self.assertEqual(parse("x"), Symbol('x'))

    def test_addition(self):
        self.assertEqual(parse("x + 1"), BinaryOp('+', Symbol('x'), Number(1)))

    def test_subtraction(self):
        self.assertEqual(parse("x - 1"), BinaryOp('-', Symbol('x'), Number(1)))

    def test_multiplication(self):
        self.assertEqual(parse("x * y"), BinaryOp('*', Symbol('x'), Symbol('y')))

    def test_division(self):
        self.assertEqual(parse("x / y"), BinaryOp('/', Symbol('x'), Symbol('y')))

    def test_power(self):
        self.assertEqual(parse("x ^ 2"), BinaryOp('^', Symbol('x'), Number(2)))

    def test_unary_minus(self):
        self.assertEqual(parse("-x"), UnaryOp('-', Symbol('x')))

    def test_double_unary_minus(self):
        self.assertEqual(parse("--x"), UnaryOp('-', UnaryOp('-', Symbol('x'))))

    def test_function_call(self):
        self.assertEqual(parse("sin(x)"), UnaryOp('sin', Symbol('x')))

    def test_parenthesized_expression(self):
        self.assertEqual(parse("(x + 1)"), BinaryOp('+', Symbol('x'), Number(1)))


class TestParserPrecedence(unittest.TestCase):
    def test_mult_before_add(self):
        # x + y * z  ->  x + (y * z)
        expected = BinaryOp('+', Symbol('x'), BinaryOp('*', Symbol('y'), Symbol('z')))
        self.assertEqual(parse("x + y * z"), expected)

    def test_parens_override_precedence(self):
        # (x + y) * z
        expected = BinaryOp('*', BinaryOp('+', Symbol('x'), Symbol('y')), Symbol('z'))
        self.assertEqual(parse("(x + y) * z"), expected)

    def test_power_right_associative(self):
        # x ^ y ^ z  ->  x ^ (y ^ z)
        expected = BinaryOp('^', Symbol('x'), BinaryOp('^', Symbol('y'), Symbol('z')))
        self.assertEqual(parse("x ^ y ^ z"), expected)

    def test_left_associative_subtraction(self):
        # x - y - z  ->  (x - y) - z
        expected = BinaryOp('-', BinaryOp('-', Symbol('x'), Symbol('y')), Symbol('z'))
        self.assertEqual(parse("x - y - z"), expected)

    def test_unary_minus_binds_tighter_than_power(self):
        # -x ^ 2  ->  (-x) ^ 2   given this grammar (unary is above power...
        # verify against YOUR grammar's precedence table as written)
        expected = BinaryOp('^', UnaryOp('-', Symbol('x')), Number(2))
        self.assertEqual(parse("-x ^ 2"), expected)

    def test_complex_expression(self):
        # x^2 + 2*x + 1
        expected = BinaryOp(
            '+',
            BinaryOp('+', BinaryOp('^', Symbol('x'), Number(2)),
                          BinaryOp('*', Number(2), Symbol('x'))),
            Number(1),
        )
        self.assertEqual(parse("x^2 + 2*x + 1"), expected)


class TestParserErrors(unittest.TestCase):
    def test_dangling_close_paren(self):
        with self.assertRaises(SyntaxError):
            parse("x + 1)")

    def test_unclosed_paren(self):
        with self.assertRaises(SyntaxError):
            parse("(x + 1")

    def test_trailing_operator(self):
        with self.assertRaises(SyntaxError):
            parse("x +")

    def test_empty_input(self):
        with self.assertRaises(SyntaxError):
            parse("")


if __name__ == '__main__':
    unittest.main()
