"""
printer.py — Converts an AST (built from ast_nodes.py) back into a
human-readable string.

Why this comes second: once you have ast_nodes.py, you have no way to
*see* what a tree looks like except __repr__, which is verbose and
unambiguous but not readable. This module gives you `to_string(tree)`
so that as you build the parser, simplifier, and differentiator, you can
sanity-check your work by eye.

This module depends ONLY on ast_nodes.py.
"""

from __future__ import annotations
from .ast_nodes import Node, Number, Symbol, BinaryOp, UnaryOp

# Precedence table — higher number binds tighter.
# Used to decide when child expressions need parentheses.
PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '^': 3,
}


def to_string(node: Node) -> str:
    """
    Convert an AST node into a readable math expression string.

    Examples (once implemented):
        Number(2)                              -> "2"
        Symbol('x')                            -> "x"
        BinaryOp('+', Symbol('x'), Number(1))  -> "x + 1"
        BinaryOp('*', BinaryOp('+', Symbol('x'), Number(1)), Symbol('y'))
                                                -> "(x + 1) * y"
        UnaryOp('-', Symbol('x'))              -> "-x"
        UnaryOp('sin', Symbol('x'))            -> "sin(x)"

    Pseudocode:
        if node is Number: return str(node.value)
        if node is Symbol: return node.name
        if node is BinaryOp:
            left_str  = _stringify_child(node, node.left,  is_left=True)
            right_str = _stringify_child(node, node.right, is_left=False)
            return f"{left_str} {node.op} {right_str}"
        if node is UnaryOp:
            if node.op == '-':
                return f"-{_stringify_child(node, node.operand, is_left=False)}"
            else:  # function call style: sin, cos, ln, exp, ...
                return f"{node.op}({to_string(node.operand)})"
        else:
            raise TypeError(f"Unknown node type: {type(node)}")
    """
    raise NotImplementedError


def _needs_parens(parent_op: str, child: Node, is_left: bool) -> bool:
    """
    Decide whether `child` needs to be wrapped in parentheses when printed
    as a child of a BinaryOp with operator `parent_op`.

    This is the trickiest part of this module. Think through these cases
    as you write it:

    1. If child is not a BinaryOp (i.e. Number, Symbol, or UnaryOp),
       it never needs parens from a precedence standpoint.
       -> return False

    2. If child IS a BinaryOp, compare PRECEDENCE[parent_op] vs
       PRECEDENCE[child.op]:
         - child precedence < parent precedence -> needs parens
           (e.g. (x + 1) * y  -- '+' is lower than '*')
         - child precedence > parent precedence -> no parens needed
           (e.g. x + y * z  -- '*' binds tighter, no parens needed)
         - child precedence == parent precedence -> depends on position
           and associativity:
             * '+' and '*' are associative, so same-precedence chains
               don't need parens regardless of side
               (e.g. x + y + z, not x + (y + z))
             * '-' and '/' are LEFT-associative but NOT associative in
               the mathematical sense: x - (y - z) != (x - y) - z
               So: if is_left is False (child is on the right) and
               parent_op is '-' or '/' and child.op has the same
               precedence -> needs parens
               (e.g. x - (y - z) must keep parens, or the meaning changes
               if you just print "x - y - z")
             * '^' is right-associative: x^(y^z) == x^y^z in most
               conventions, but (x^y)^z is different. So parens logic
               flips: right side rarely needs parens, left side might.
               For this scaffold, keep it simple: always parenthesize a
               '^' left child that is itself a BinaryOp with '^', and
               never parenthesize the right child.

    Work through several examples on paper before implementing — this
    function is where subtle bugs hide.
    """
    raise NotImplementedError


def _stringify_child(parent: BinaryOp, child: Node, is_left: bool) -> str:
    """
    Render `child` as a string, wrapping in parentheses if
    _needs_parens says so.

    Pseudocode:
        s = to_string(child)
        if _needs_parens(parent.op, child, is_left):
            return f"({s})"
        return s
    """
    raise NotImplementedError
