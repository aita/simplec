import attr


@attr.s(slots=True)
class Node:
    pass


@attr.s(slots=True)
class Stmt(Node):
    pass


@attr.s(slots=True)
class Expr(Stmt):
    pass


@attr.s(slots=True)
class Number(Expr):
    literal = attr.ib()


@attr.s(slots=True)
class Name(Expr):
    name = attr.ib()
    offset = attr.ib()
    is_lvar = attr.ib(default=False)


@attr.s(slots=True)
class Unary(Expr):
    operator = attr.ib()
    operand = attr.ib()


@attr.s(slots=True)
class Binary(Expr):
    operator = attr.ib()
    left = attr.ib()
    right = attr.ib()


@attr.s(slots=True)
class Paren(Expr):
    operand = attr.ib()
