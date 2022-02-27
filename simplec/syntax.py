import attr


@attr.s(slots=True)
class Position:
    start = attr.ib()
    end = attr.ib()
    line = attr.ib()
    column = attr.ib()


@attr.s(slots=True)
class Symbol:
    name = attr.ib()
    pos = attr.ib()


@attr.s(slots=True)
class Scope:
    parent = attr.ib()
    children = attr.ib(factory=list)
    symbols = attr.ib(factory=dict)

    def find_name(self, name):
        if name in self.symbols:
            return name
        if self.parent:
            return self.parent.find_name(name)
        return None


class Stmt:
    pass


@attr.s(slots=True)
class CompoundStmt(Stmt):
    stmts = attr.ib()
    scope = attr.ib()


@attr.s(slots=True)
class ReturnStmt(Stmt):
    expr = attr.ib()


@attr.s(slots=True)
class IfStmt(Stmt):
    condition = attr.ib()
    then_stmt = attr.ib()
    else_stmt = attr.ib()


@attr.s(slots=True)
class WhileStmt(Stmt):
    condition = attr.ib()
    stmt = attr.ib()


class Expr(Stmt):
    pass


class ExprMeta(type):
    def __new__(cls, name, bases, namespace):
        new_cls = super().__new__(cls, name, bases, namespace)
        new_cls.is_lvar = attr.ib(default=False)
        # new_cls.pos = attr.ib(default=None)
        return new_cls


@attr.s(slots=True)
class Constant(Expr, metaclass=ExprMeta):
    literal = attr.ib()


@attr.s(slots=True)
class NameExpr(Expr, metaclass=ExprMeta):
    name = attr.ib()
    offset = attr.ib(default=None)


@attr.s(slots=True)
class UnaryExpr(Expr, metaclass=ExprMeta):
    operator = attr.ib()
    operand = attr.ib()


@attr.s(slots=True)
class BinaryExpr(Expr, metaclass=ExprMeta):
    operator = attr.ib()
    left = attr.ib()
    right = attr.ib()


@attr.s(slots=True)
class ParenExpr(Expr, metaclass=ExprMeta):
    expr = attr.ib()


class Decl:
    pass


@attr.s(slots=True)
class FunctionDecl:
    name = attr.ib()
    body = attr.ib()
    scope = attr.ib()
