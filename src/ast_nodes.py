"""
ast_nodes.py — Abstract Syntax Tree node definitions for the CAS.

Every expression in this system is represented as a tree of Node objects.
This module has ZERO dependencies on the other modules — it is pure data
structure. Get this right and everything downstream becomes easier.

Design notes:
- Nodes should be immutable in spirit (don't mutate a node's children after
  construction; build new nodes instead). This matters a lot once you write
  the simplifier, which constructs new trees rather than editing in place.
- __eq__ must do STRUCTURAL equality (two separately-built trees representing
  the same expression should be ==). This is what most of the test suite
  checks against.
- __repr__ should be unambiguous (for debugging), not pretty. Pretty
  printing is printer.py's job.
- __hash__ is needed because simplification rules may use nodes as dict keys
  or put them in sets (e.g. collecting like terms). Since these are meant to
  be immutable, hashing is safe.
"""

from __future__ import annotations
from typing import Union


class Node:
    """
    Base class for all AST nodes. Not meant to be instantiated directly.
    """

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    def __hash__(self) -> int:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError


class Number(Node):
    """
    A numeric constant, e.g. 2, -5, 3.14.

    Pseudocode:
        store `value` (int or float)

    __eq__: two Numbers are equal if their values are equal
    __hash__: hash(('Number', self.value))
    __repr__: f"Number({self.value})"
    """

    def __init__(self, value: Union[int, float]):
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    def __hash__(self) -> int:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError


class Symbol(Node):
    """
    A variable, e.g. x, y, theta.

    Pseudocode:
        store `name` (str)

    __eq__: two Symbols are equal if their names are equal
    __hash__: hash(('Symbol', self.name))
    __repr__: f"Symbol({self.name!r})"
    """

    def __init__(self, name: str):
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    def __hash__(self) -> int:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError


class BinaryOp(Node):
    """
    A binary operation: left <op> right.
    Supported ops (as strings): '+', '-', '*', '/', '^'

    Pseudocode:
        validate op is one of the supported operators, else raise ValueError
        store `op`, `left` (Node), `right` (Node)

    __eq__: same op AND left == left AND right == right
        NOTE: for '+' and '*' you might be tempted to treat operand order as
        irrelevant (commutativity) here — DON'T. Structural equality means
        exact tree shape. Commutative reordering belongs in the simplifier,
        not in equality. Keeping this strict is what makes the simplifier
        testable in isolation.
    __hash__: hash(('BinaryOp', self.op, self.left, self.right))
    __repr__: f"BinaryOp({self.op!r}, {self.left!r}, {self.right!r})"
    """

    VALID_OPS = {'+', '-', '*', '/', '^'}

    def __init__(self, op: str, left: Node, right: Node):
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    def __hash__(self) -> int:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError


class UnaryOp(Node):
    """
    A unary operation, e.g. negation (-x) or a named function call
    like sin(x), cos(x), ln(x), exp(x).

    Pseudocode:
        store `op` (str, e.g. '-', 'sin', 'cos', 'ln', 'exp')
        store `operand` (Node)

    __eq__: same op AND operand == operand
    __hash__: hash(('UnaryOp', self.op, self.operand))
    __repr__: f"UnaryOp({self.op!r}, {self.operand!r})"
    """

    def __init__(self, op: str, operand: Node):
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    def __hash__(self) -> int:
        raise NotImplementedError

    def __repr__(self) -> str:
        raise NotImplementedError
