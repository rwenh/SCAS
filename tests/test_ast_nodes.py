import unittest
from src.ast_nodes import Number, Symbol, BinaryOp, UnaryOp


class TestNumber(unittest.TestCase):
    def test_construction(self):
        n = Number(5)
        self.assertEqual(n.value, 5)

    def test_equality_same_value(self):
        self.assertEqual(Number(3), Number(3))

    def test_equality_different_value(self):
        self.assertNotEqual(Number(3), Number(4))

    def test_equality_int_vs_float(self):
        # 3 == 3.0 in Python; decide if your Number treats these as equal
        self.assertEqual(Number(3), Number(3.0))

    def test_hashable(self):
        s = {Number(1), Number(1), Number(2)}
        self.assertEqual(len(s), 2)

    def test_repr(self):
        self.assertEqual(repr(Number(5)), "Number(5)")


class TestSymbol(unittest.TestCase):
    def test_construction(self):
        s = Symbol("x")
        self.assertEqual(s.name, "x")

    def test_equality_same_name(self):
        self.assertEqual(Symbol("x"), Symbol("x"))

    def test_equality_different_name(self):
        self.assertNotEqual(Symbol("x"), Symbol("y"))

    def test_hashable(self):
        s = {Symbol("x"), Symbol("x"), Symbol("y")}
        self.assertEqual(len(s), 2)

    def test_repr(self):
        self.assertEqual(repr(Symbol("x")), "Symbol('x')")


class TestBinaryOp(unittest.TestCase):
    def test_construction(self):
        node = BinaryOp('+', Symbol('x'), Number(1))
        self.assertEqual(node.op, '+')
        self.assertEqual(node.left, Symbol('x'))
        self.assertEqual(node.right, Number(1))

    def test_invalid_op_raises(self):
        with self.assertRaises(ValueError):
            BinaryOp('%', Symbol('x'), Number(1))

    def test_equality_structural(self):
        a = BinaryOp('+', Symbol('x'), Number(1))
        b = BinaryOp('+', Symbol('x'), Number(1))
        self.assertEqual(a, b)

    def test_equality_different_op(self):
        a = BinaryOp('+', Symbol('x'), Number(1))
        b = BinaryOp('-', Symbol('x'), Number(1))
        self.assertNotEqual(a, b)

    def test_equality_operand_order_matters(self):
        # x + 1 should NOT equal 1 + x structurally (that's the
        # simplifier's job, not __eq__'s)
        a = BinaryOp('+', Symbol('x'), Number(1))
        b = BinaryOp('+', Number(1), Symbol('x'))
        self.assertNotEqual(a, b)

    def test_nested_equality(self):
        a = BinaryOp('*', BinaryOp('+', Symbol('x'), Number(1)), Symbol('y'))
        b = BinaryOp('*', BinaryOp('+', Symbol('x'), Number(1)), Symbol('y'))
        self.assertEqual(a, b)

    def test_hashable(self):
        a = BinaryOp('+', Symbol('x'), Number(1))
        b = BinaryOp('+', Symbol('x'), Number(1))
        self.assertEqual(len({a, b}), 1)


class TestUnaryOp(unittest.TestCase):
    def test_construction(self):
        node = UnaryOp('-', Symbol('x'))
        self.assertEqual(node.op, '-')
        self.assertEqual(node.operand, Symbol('x'))

    def test_equality(self):
        self.assertEqual(UnaryOp('sin', Symbol('x')), UnaryOp('sin', Symbol('x')))

    def test_equality_different_op(self):
        self.assertNotEqual(UnaryOp('sin', Symbol('x')), UnaryOp('cos', Symbol('x')))

    def test_equality_different_operand(self):
        self.assertNotEqual(UnaryOp('sin', Symbol('x')), UnaryOp('sin', Symbol('y')))

    def test_hashable(self):
        s = {UnaryOp('-', Symbol('x')), UnaryOp('-', Symbol('x'))}
        self.assertEqual(len(s), 1)


if __name__ == '__main__':
    unittest.main()
