import attr


class Stmt:
    pass


class Expr(Stmt):
    pass


class ExprMeta(type):
    def __new__(cls, name, bases, namespace):
        new_cls = super().__new__(cls, name, bases, namespace)
        new_cls.is_lvar = attr.ib(default=False)
        # new_cls.pos = attr.ib(default=None)
        return new_cls


@attr.s(slots=True)
class Number(Expr, metaclass=ExprMeta):
    literal = attr.ib()


@attr.s(slots=True)
class Name(Expr, metaclass=ExprMeta):
    name = attr.ib()
    offset = attr.ib()


@attr.s(slots=True)
class Unary(Expr, metaclass=ExprMeta):
    operator = attr.ib()
    operand = attr.ib()


@attr.s(slots=True)
class Binary(Expr, metaclass=ExprMeta):
    operator = attr.ib()
    left = attr.ib()
    right = attr.ib()


@attr.s(slots=True)
class Paren(Expr, metaclass=ExprMeta):
    operand = attr.ib()
