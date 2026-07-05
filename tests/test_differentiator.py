import unittest
from src.ast_nodes import Number, Symbol, BinaryOp, UnaryOp
from src.differentiator import differentiate


class TestBasicRules(unittest.TestCase):
    def test_derivative_of_constant(self):
        self.assertEqual(differentiate(Number(5), 'x'), Number(0))

    def test_derivative_of_var_wrt_itself(self):
        self.assertEqual(differentiate(Symbol('x'), 'x'), Number(1))

    def test_derivative_of_other_var(self):
        self.assertEqual(differentiate(Symbol('y'), 'x'), Number(0))


class TestSumAndDifferenceRules(unittest.TestCase):
    def test_sum_rule(self):
        # d(x + y)/dx = 1 + 0
        node = BinaryOp('+', Symbol('x'), Symbol('y'))
        expected = BinaryOp('+', Number(1), Number(0))
        self.assertEqual(differentiate(node, 'x'), expected)

    def test_difference_rule(self):
        node = BinaryOp('-', Symbol('x'), Symbol('y'))
        expected = BinaryOp('-', Number(1), Number(0))
        self.assertEqual(differentiate(node, 'x'), expected)


class TestProductRule(unittest.TestCase):
    def test_product_rule_structure(self):
        # d(x * y)/dx = 1*y + x*0
        node = BinaryOp('*', Symbol('x'), Symbol('y'))
        expected = BinaryOp(
            '+',
            BinaryOp('*', Number(1), Symbol('y')),
            BinaryOp('*', Symbol('x'), Number(0)),
        )
        self.assertEqual(differentiate(node, 'x'), expected)


class TestQuotientRule(unittest.TestCase):
    def test_quotient_rule_structure(self):
        # d(x / y)/dx = (1*y - x*0) / y^2
        node = BinaryOp('/', Symbol('x'), Symbol('y'))
        expected = BinaryOp(
            '/',
            BinaryOp('-', BinaryOp('*', Number(1), Symbol('y')),
                          BinaryOp('*', Symbol('x'), Number(0))),
            BinaryOp('^', Symbol('y'), Number(2)),
        )
        self.assertEqual(differentiate(node, 'x'), expected)


class TestPowerRule(unittest.TestCase):
    def test_power_rule_constant_exponent(self):
        # d(x^3)/dx = 3 * x^2 * 1
        node = BinaryOp('^', Symbol('x'), Number(3))
        expected = BinaryOp(
            '*',
            BinaryOp('*', Number(3), BinaryOp('^', Symbol('x'), Number(2))),
            Number(1),
        )
        self.assertEqual(differentiate(node, 'x'), expected)

    def test_power_rule_variable_exponent_not_implemented(self):
        # x^x is out of scope for this scaffold — must raise, not silently
        # produce a wrong answer
        node = BinaryOp('^', Symbol('x'), Symbol('x'))
        with self.assertRaises(NotImplementedError):
            differentiate(node, 'x')


class TestChainRuleFunctions(unittest.TestCase):
    def test_sin(self):
        node = UnaryOp('sin', Symbol('x'))
        expected = BinaryOp('*', UnaryOp('cos', Symbol('x')), Number(1))
        self.assertEqual(differentiate(node, 'x'), expected)

    def test_cos(self):
        node = UnaryOp('cos', Symbol('x'))
        expected = BinaryOp('*', UnaryOp('-', UnaryOp('sin', Symbol('x'))), Number(1))
        self.assertEqual(differentiate(node, 'x'), expected)

    def test_tan(self):
        node = UnaryOp('tan', Symbol('x'))
        expected = BinaryOp('/', Number(1), BinaryOp('^', UnaryOp('cos', Symbol('x')), Number(2)))
        self.assertEqual(differentiate(node, 'x'), expected)

    def test_ln(self):
        node = UnaryOp('ln', Symbol('x'))
        expected = BinaryOp('/', Number(1), Symbol('x'))
        self.assertEqual(differentiate(node, 'x'), expected)

    def test_exp(self):
        node = UnaryOp('exp', Symbol('x'))
        expected = BinaryOp('*', UnaryOp('exp', Symbol('x')), Number(1))
        self.assertEqual(differentiate(node, 'x'), expected)

    def test_sqrt(self):
        node = UnaryOp('sqrt', Symbol('x'))
        expected = BinaryOp('/', Number(1), BinaryOp('*', Number(2), UnaryOp('sqrt', Symbol('x'))))
        self.assertEqual(differentiate(node, 'x'), expected)

    def test_negation(self):
        node = UnaryOp('-', Symbol('x'))
        self.assertEqual(differentiate(node, 'x'), UnaryOp('-', Number(1)))


class TestChainRuleComposition(unittest.TestCase):
    def test_sin_of_x_squared(self):
        # d(sin(x^2))/dx = cos(x^2) * d(x^2)/dx
        inner = BinaryOp('^', Symbol('x'), Number(2))
        node = UnaryOp('sin', inner)
        d_inner = differentiate(inner, 'x')
        expected = BinaryOp('*', UnaryOp('cos', inner), d_inner)
        self.assertEqual(differentiate(node, 'x'), expected)


if __name__ == '__main__':
    unittest.main()
