import unittest
from src.ast_nodes import Number, Symbol, BinaryOp, UnaryOp
from src.printer import to_string


class TestBasicPrinting(unittest.TestCase):
    def test_number(self):
        self.assertEqual(to_string(Number(5)), "5")

    def test_symbol(self):
        self.assertEqual(to_string(Symbol('x')), "x")

    def test_simple_addition(self):
        self.assertEqual(to_string(BinaryOp('+', Symbol('x'), Number(1))), "x + 1")

    def test_simple_multiplication(self):
        self.assertEqual(to_string(BinaryOp('*', Symbol('x'), Symbol('y'))), "x * y")

    def test_unary_negation(self):
        self.assertEqual(to_string(UnaryOp('-', Symbol('x'))), "-x")

    def test_function_call(self):
        self.assertEqual(to_string(UnaryOp('sin', Symbol('x'))), "sin(x)")

    def test_nested_function_call(self):
        self.assertEqual(to_string(UnaryOp('ln', UnaryOp('sin', Symbol('x')))), "ln(sin(x))")


class TestParenthesization(unittest.TestCase):
    def test_mult_of_addition_needs_parens_left(self):
        node = BinaryOp('*', BinaryOp('+', Symbol('x'), Number(1)), Symbol('y'))
        self.assertEqual(to_string(node), "(x + 1) * y")

    def test_mult_of_addition_needs_parens_right(self):
        node = BinaryOp('*', Symbol('y'), BinaryOp('+', Symbol('x'), Number(1)))
        self.assertEqual(to_string(node), "y * (x + 1)")

    def test_addition_of_mult_no_parens_needed(self):
        node = BinaryOp('+', BinaryOp('*', Symbol('x'), Number(2)), Symbol('y'))
        self.assertEqual(to_string(node), "x * 2 + y")

    def test_same_precedence_addition_chain_no_parens(self):
        node = BinaryOp('+', BinaryOp('+', Symbol('x'), Symbol('y')), Symbol('z'))
        self.assertEqual(to_string(node), "x + y + z")

    def test_subtraction_right_associativity_needs_parens(self):
        # x - (y - z) must keep parens, meaning changes otherwise
        node = BinaryOp('-', Symbol('x'), BinaryOp('-', Symbol('y'), Symbol('z')))
        self.assertEqual(to_string(node), "x - (y - z)")

    def test_subtraction_left_chain_no_parens(self):
        # (x - y) - z prints without parens: left-associative default
        node = BinaryOp('-', BinaryOp('-', Symbol('x'), Symbol('y')), Symbol('z'))
        self.assertEqual(to_string(node), "x - y - z")

    def test_division_right_needs_parens(self):
        node = BinaryOp('/', Symbol('x'), BinaryOp('/', Symbol('y'), Symbol('z')))
        self.assertEqual(to_string(node), "x / (y / z)")

    def test_power_left_needs_parens(self):
        node = BinaryOp('^', BinaryOp('^', Symbol('x'), Symbol('y')), Symbol('z'))
        self.assertEqual(to_string(node), "(x ^ y) ^ z")

    def test_power_right_no_parens(self):
        node = BinaryOp('^', Symbol('x'), BinaryOp('^', Symbol('y'), Symbol('z')))
        self.assertEqual(to_string(node), "x ^ y ^ z")

    def test_power_binds_tighter_than_mult(self):
        node = BinaryOp('*', BinaryOp('^', Symbol('x'), Number(2)), Symbol('y'))
        self.assertEqual(to_string(node), "x ^ 2 * y")


class TestRoundTrip(unittest.TestCase):
    def test_complex_expression(self):
        # (x + 1) * (x - 1)
        node = BinaryOp(
            '*',
            BinaryOp('+', Symbol('x'), Number(1)),
            BinaryOp('-', Symbol('x'), Number(1)),
        )
        self.assertEqual(to_string(node), "(x + 1) * (x - 1)")


if __name__ == '__main__':
    unittest.main()
