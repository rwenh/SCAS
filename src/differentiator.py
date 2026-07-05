"""
differentiator.py — Symbolic differentiation.

Takes an AST and a variable name, and returns a new AST representing the
derivative with respect to that variable. Does NOT simplify the result —
that's simplifier.py's job. Compose them: simplify(differentiate(expr, 'x'))

Depends on: ast_nodes.py
(simplifier.py is used downstream, not by this module directly)
"""

from __future__ import annotations
import math
from .ast_nodes import Node, Number, Symbol, BinaryOp, UnaryOp


def differentiate(node: Node, var: str) -> Node:
    """
    Compute d(node)/d(var) symbolically, returning a new (unsimplified) AST.

    Pseudocode — dispatch on node type:

        if node is Number:
            return Number(0)                 # derivative of a constant

        if node is Symbol:
            if node.name == var:
                return Number(1)              # d(x)/dx = 1
            else:
                return Number(0)              # d(y)/dx = 0, y treated as constant

        if node is BinaryOp:
            return _differentiate_binary(node, var)

        if node is UnaryOp:
            return _differentiate_unary(node, var)

        raise TypeError(f"Unknown node type: {type(node)}")
    """
    raise NotImplementedError


def _differentiate_binary(node: BinaryOp, var: str) -> Node:
    """
    Apply the correct differentiation rule based on node.op.
    Let u = node.left, v = node.right, u' = differentiate(u, var),
    v' = differentiate(v, var).

    Sum rule:
        d(u + v)/dx = u' + v'
        -> BinaryOp('+', du, dv)

    Difference rule:
        d(u - v)/dx = u' - v'
        -> BinaryOp('-', du, dv)

    Product rule:
        d(u * v)/dx = u'*v + u*v'
        -> BinaryOp('+', BinaryOp('*', du, v), BinaryOp('*', u, dv))
        NOTE: use the ORIGINAL u and v (not their derivatives) in the
        cross terms — a common transcription slip is reusing du/dv where
        u/v belong.

    Quotient rule:
        d(u / v)/dx = (u'*v - u*v') / v^2
        -> BinaryOp('/',
                     BinaryOp('-', BinaryOp('*', du, v), BinaryOp('*', u, dv)),
                     BinaryOp('^', v, Number(2)))

    Power rule — this one has TWO cases depending on what's in the exponent:

        Case A: exponent is a constant Number (the common case, e.g. x^3)
            d(u^n)/dx = n * u^(n-1) * u'
            -> BinaryOp('*',
                         BinaryOp('*', Number(n), BinaryOp('^', u, Number(n-1))),
                         du)

        Case B: exponent is NOT constant (e.g. x^x, or a^u where u depends
        on var) — general exponential differentiation via logarithmic
        differentiation is out of scope for this scaffold. For this
        project, only support Case A; if the exponent is not a Number,
        raise NotImplementedError with a clear message explaining that
        variable exponents aren't supported yet. (This is a deliberate,
        documented scope cut — not a bug.)

    Pseudocode:
        u, v = node.left, node.right
        du = differentiate(u, var)
        dv = differentiate(v, var)

        if node.op == '+': ...
        elif node.op == '-': ...
        elif node.op == '*': ...
        elif node.op == '/': ...
        elif node.op == '^':
            if not isinstance(node.right, Number):
                raise NotImplementedError(...)
            ...
        else:
            raise ValueError(f"Unknown operator: {node.op}")
    """
    raise NotImplementedError


def _differentiate_unary(node: UnaryOp, var: str) -> Node:
    """
    Apply the chain rule for negation and named functions.
    Let u = node.operand, u' = differentiate(u, var).

    Negation:
        d(-u)/dx = -u'
        -> UnaryOp('-', du)

    Chain rule for functions — d(f(u))/dx = f'(u) * u':

        sin(u):  d/dx = cos(u) * u'
            -> BinaryOp('*', UnaryOp('cos', u), du)

        cos(u):  d/dx = -sin(u) * u'
            -> BinaryOp('*', UnaryOp('-', UnaryOp('sin', u)), du)

        tan(u):  d/dx = u' / cos(u)^2
            -> BinaryOp('/', du, BinaryOp('^', UnaryOp('cos', u), Number(2)))

        ln(u):   d/dx = u' / u
            -> BinaryOp('/', du, u)

        exp(u):  d/dx = exp(u) * u'
            -> BinaryOp('*', UnaryOp('exp', u), du)

        sqrt(u): d/dx = u' / (2 * sqrt(u))
            -> BinaryOp('/', du, BinaryOp('*', Number(2), UnaryOp('sqrt', u)))

    Pseudocode:
        u = node.operand
        du = differentiate(u, var)

        if node.op == '-':
            return UnaryOp('-', du)

        # dispatch table style is cleaner than a long if/elif chain here —
        # consider a dict mapping op name -> a small builder function once
        # you've written all six cases and see the repetition
        if node.op == 'sin': ...
        elif node.op == 'cos': ...
        elif node.op == 'tan': ...
        elif node.op == 'ln': ...
        elif node.op == 'exp': ...
        elif node.op == 'sqrt': ...
        else:
            raise ValueError(f"Unknown function: {node.op}")
    """
    raise NotImplementedError
