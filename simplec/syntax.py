import attr


@attr.s(slots=True)
class Position:
    start = attr.ib()
    end = attr.ib()
    line = attr.ib()
    column = attr.ib()


@attr.s(slots=True, eq=False)
class Symbol:
    name = attr.ib()
    decl = attr.ib()
    pos = attr.ib()


@attr.s(slots=True)
class Scope:
    parent = attr.ib()
    children = attr.ib(factory=list)
    symbols = attr.ib(factory=dict)

    def find_name(self, name):
        if name in self.symbols:
            return self.symbols[name]
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
    symbol = attr.ib()


@attr.s(slots=True)
class CallExpr(Expr, metaclass=ExprMeta):
    expr = attr.ib()
    args = attr.ib()


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
class FunctionDecl(Decl):
    name = attr.ib()
    params = attr.ib()
    body = attr.ib()
    scope = attr.ib()
    symbol = attr.ib()


@attr.s(slots=True)
class ParamDecl(Decl):
    name = attr.ib()
    symbol = attr.ib()
