import unittest
from src.ast_nodes import Number, Symbol, BinaryOp, UnaryOp
from src.simplifier import simplify


class TestConstantFolding(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(simplify(BinaryOp('+', Number(2), Number(3))), Number(5))

    def test_subtraction(self):
        self.assertEqual(simplify(BinaryOp('-', Number(5), Number(3))), Number(2))

    def test_multiplication(self):
        self.assertEqual(simplify(BinaryOp('*', Number(4), Number(3))), Number(12))

    def test_division(self):
        self.assertEqual(simplify(BinaryOp('/', Number(6), Number(3))), Number(2))

    def test_division_by_zero_raises(self):
        with self.assertRaises(ZeroDivisionError):
            simplify(BinaryOp('/', Number(1), Number(0)))

    def test_power(self):
        self.assertEqual(simplify(BinaryOp('^', Number(2), Number(3))), Number(8))

    def test_nested_constants(self):
        # (2 + 3) * 4  ->  20
        node = BinaryOp('*', BinaryOp('+', Number(2), Number(3)), Number(4))
        self.assertEqual(simplify(node), Number(20))


class TestAdditionIdentities(unittest.TestCase):
    def test_x_plus_zero(self):
        self.assertEqual(simplify(BinaryOp('+', Symbol('x'), Number(0))), Symbol('x'))

    def test_zero_plus_x(self):
        self.assertEqual(simplify(BinaryOp('+', Number(0), Symbol('x'))), Symbol('x'))


class TestSubtractionIdentities(unittest.TestCase):
    def test_x_minus_zero(self):
        self.assertEqual(simplify(BinaryOp('-', Symbol('x'), Number(0))), Symbol('x'))

    def test_x_minus_x(self):
        self.assertEqual(simplify(BinaryOp('-', Symbol('x'), Symbol('x'))), Number(0))


class TestMultiplicationIdentities(unittest.TestCase):
    def test_x_times_zero(self):
        self.assertEqual(simplify(BinaryOp('*', Symbol('x'), Number(0))), Number(0))

    def test_zero_times_x(self):
        self.assertEqual(simplify(BinaryOp('*', Number(0), Symbol('x'))), Number(0))

    def test_x_times_one(self):
        self.assertEqual(simplify(BinaryOp('*', Symbol('x'), Number(1))), Symbol('x'))

    def test_one_times_x(self):
        self.assertEqual(simplify(BinaryOp('*', Number(1), Symbol('x'))), Symbol('x'))


class TestDivisionIdentities(unittest.TestCase):
    def test_x_over_one(self):
        self.assertEqual(simplify(BinaryOp('/', Symbol('x'), Number(1))), Symbol('x'))

    def test_zero_over_x(self):
        self.assertEqual(simplify(BinaryOp('/', Number(0), Symbol('x'))), Number(0))


class TestPowerIdentities(unittest.TestCase):
    def test_x_to_zero(self):
        self.assertEqual(simplify(BinaryOp('^', Symbol('x'), Number(0))), Number(1))

    def test_x_to_one(self):
        self.assertEqual(simplify(BinaryOp('^', Symbol('x'), Number(1))), Symbol('x'))

    def test_one_to_x(self):
        self.assertEqual(simplify(BinaryOp('^', Number(1), Symbol('x'))), Number(1))

    def test_zero_to_x(self):
        self.assertEqual(simplify(BinaryOp('^', Number(0), Symbol('x'))), Number(0))


class TestUnarySimplification(unittest.TestCase):
    def test_double_negation(self):
        self.assertEqual(simplify(UnaryOp('-', UnaryOp('-', Symbol('x')))), Symbol('x'))

    def test_negate_constant(self):
        self.assertEqual(simplify(UnaryOp('-', Number(5))), Number(-5))

    def test_sin_zero(self):
        self.assertEqual(simplify(UnaryOp('sin', Number(0))), Number(0))

    def test_cos_zero(self):
        self.assertEqual(simplify(UnaryOp('cos', Number(0))), Number(1))

    def test_ln_one(self):
        self.assertEqual(simplify(UnaryOp('ln', Number(1))), Number(0))

    def test_exp_zero(self):
        self.assertEqual(simplify(UnaryOp('exp', Number(0))), Number(1))

    def test_sin_symbolic_unchanged(self):
        self.assertEqual(simplify(UnaryOp('sin', Symbol('x'))), UnaryOp('sin', Symbol('x')))


class TestFixedPointIteration(unittest.TestCase):
    def test_requires_multiple_passes(self):
        # (x + 0) * (1 * y)  ->  x * y, needs two passes to fully resolve
        node = BinaryOp(
            '*',
            BinaryOp('+', Symbol('x'), Number(0)),
            BinaryOp('*', Number(1), Symbol('y')),
        )
        self.assertEqual(simplify(node), BinaryOp('*', Symbol('x'), Symbol('y')))

    def test_deeply_nested_identity_chain(self):
        # ((x + 0) + 0) + 0  ->  x
        node = BinaryOp('+', BinaryOp('+', BinaryOp('+', Symbol('x'), Number(0)), Number(0)), Number(0))
        self.assertEqual(simplify(node), Symbol('x'))


if __name__ == '__main__':
    unittest.main()
