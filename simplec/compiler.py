import attr

from .syntax import (
    BinaryExpr,
    CallExpr,
    CompoundStmt,
    Constant,
    Expr,
    FunctionDecl,
    IfStmt,
    NameExpr,
    ParamDecl,
    ParenExpr,
    ReturnStmt,
    UnaryExpr,
    WhileStmt,
)


@attr.s(slots=True)
class Var:
    name = attr.ib()
    symbol = attr.ib()
    offset = attr.ib()


@attr.s(slots=True)
class Frame:
    size = attr.ib()
    vars = attr.ib(factory=dict)

    def get_offset(self, symbol):
        return self.vars[symbol].offset



def indirect(reg, offset=0):
    if offset != 0:
        return f"[{reg}, #{offset}]"
    else:
        return f"[{reg}]"


def regset(*regs):
    s = ", ".join(regs)
    return f"{{{s}}}"


class Compiler:
    def __init__(self, output):
        self.output = output
        self.label_count = 0
        self.frame = None

    def print(self, *args):
        print(*args, file=self.output)

    def build_frame(self, func, offset):
        vars = {}
        local_offset = offset

        def _visit(scope):
            nonlocal local_offset
            for name, symbol in scope.symbols.items():
                if func.symbol == symbol:
                    continue
                match symbol.decl:
                    case ParamDecl():
                        pass
                    case _:
                        vars[symbol] = Var(
                            name=name,
                            symbol=symbol,
                            offset=local_offset,
                        )
                        local_offset -= 4

            for child in scope.children:
                _visit(child)

        _visit(func.scope)

        reg_params = func.params[:4]
        stack_params = func.params[4:]
        for param in reg_params:
            vars[param.symbol] = Var(
                name=param.name,
                symbol=param.symbol,
                offset=local_offset,
            )
            local_offset -= 4

        stack_param_offset = 4
        for param in stack_params:
            symbol = param.symbol
            vars[symbol] = Var(
                name=param.name,
                symbol=symbol,
                offset=stack_param_offset,
            )
            stack_param_offset += 4

        return Frame(vars=vars, size=-local_offset)

    def emit(self, mnemonic, *operands):
        def to_str(operand):
            if isinstance(operand, str):
                return operand
            if isinstance(operand, int):
                return f"#{operand}"
            return str(operand)

        self.print(f"\t{mnemonic}\t{', '.join(to_str(operand) for operand in operands)}")

    def emit_label(self, label):
        self.print(f"{label}:")

    def gen_label(self, name):
        label = f"L_{name}_{self.label_count}"
        self.label_count += 1
        return label

    def compile(self, program):
        for decl in program:
            self.emit_external_definition(decl)

    def emit_external_definition(self, decl):
        match decl:
            case FunctionDecl() as func:
                self.emit_function_decl(func)

    def emit_function_decl(self, func):
        self.frame = self.build_frame(func, offset=-12)
        frame_size = self.frame.size
        self.return_label = self.gen_label("return")

        self.print(f".globl {func.name}")
        self.emit_label(func.name)
        self.emit("push", regset("fp", "lr"))
        self.emit("add", "fp", "sp", 4)
        self.emit("sub", "sp", "sp", frame_size)
        self.emit("str", "r4", indirect("fp", -8))
        reg_params = func.params[:4]
        for i, param in enumerate(reg_params):
            self.emit("str", f"r{i}", indirect("fp", self.frame.get_offset(param.symbol)))
        for stmt in func.body.stmts:
            self.emit_stmt(stmt)
        self.emit_label(self.return_label)
        self.emit("ldr", "r4", indirect("fp", -8))
        self.emit("sub", "sp", "fp", 4)
        self.emit("pop", regset("fp", "pc"))

    def emit_stmt(self, stmt):
        match stmt:
            case Expr() as expr:
                self.emit_expr(expr)
            case ReturnStmt(expr=None):
                self.emit("b", self.return_label)
            case ReturnStmt(expr=expr):
                self.emit_expr(expr)
                self.emit("b", self.return_label)
            case CompoundStmt(stmts=stmts):
                for stmt in stmts:
                    self.emit_stmt(stmt)
            case IfStmt(condition=condition, then_stmt=then_stmt, else_stmt=None):
                end_label = self.gen_label("end")
                self.emit_expr(condition)
                self.emit("cmp", "r0", 0)
                self.emit("beq", end_label)
                self.emit_stmt(then_stmt)
                self.emit_label(end_label)
            case IfStmt(condition=condition, then_stmt=then_stmt, else_stmt=else_stmt):
                else_label = self.gen_label("else")
                end_label = self.gen_label("end")
                self.emit_expr(condition)
                self.emit("cmp", "r0", 0)
                self.emit("beq", else_label)
                self.emit_stmt(then_stmt)
                self.emit("b", end_label)
                self.emit_label(else_label)
                self.emit_stmt(else_stmt)
                self.emit_label(end_label)
            case WhileStmt(condition=condition, stmt=stmt):
                begin_label = self.gen_label("begin")
                end_label = self.gen_label("end")
                self.emit_label(begin_label)
                self.emit_expr(condition)
                self.emit("cmp", "r0", 0)
                self.emit("beq", end_label)
                self.emit_stmt(stmt)
                self.emit("b", begin_label)
                self.emit_label(end_label)
            case _:
                raise ValueError(f"unknown stmt: {stmt}")

    def emit_expr(self, expr):
        match expr:
            case NameExpr():
                offset = self.frame.get_offset(expr.symbol)
                self.emit("ldr", "r0", indirect("fp", offset))
            case Constant(literal=literal):
                self.emit("mov", "r0", int(literal))
            case ParenExpr(expr=expr):
                self.emit_expr(expr)
            case CallExpr():
                return self.emit_call_expr(expr)
            case UnaryExpr(operator=op, operand=operand):
                match op:
                    case "+":
                        self.emit_expr(operand)
                    case "-":
                        self.emit_expr(operand)
                        self.emit("neg", "r0")
                    case '&':
                        match operand:
                            case NameExpr():
                                offset = self.frame.get_offset(operand.symbol)
                                if offset > 0:
                                    self.emit("add", "r0", "fp", offset)
                                else:
                                    self.emit("sub", "r0", "fp", -offset)
                            case _:
                                raise ValueError("the expression is not addressable")
                    case '*':
                        offset = self.frame.get_offset(operand.symbol)
                        self.emit("ldr", "r0", indirect("r0"))
                    case _:
                        raise ValueError(f"unknown unary operator: {op}")
            case BinaryExpr(operator="=", left=left, right=right):
                if not left.is_lvar:
                    raise ValueError("LHS is not lvar")
                offset = self.frame.get_offset(left.symbol)
                right = self.emit_expr(right)
                self.emit("str", "r0", indirect("fp", offset))
            case BinaryExpr(operator=op, left=left, right=right):
                left = self.emit_expr(left)
                self.emit("push", regset("r0"))
                right = self.emit_expr(right)
                match op:
                    case "+":
                        self.emit("pop", regset("r4"))
                        self.emit("add", "r0", "r4", "r0")
                    case "-":
                        self.emit("pop", regset("r4"))
                        self.emit("sub", "r0", "r4", "r0")
                    case "*":
                        self.emit("pop", regset("r4"))
                        self.emit("mul", "r0", "r4", "r0")
                    case "/":
                        self.emit("pop", regset("r4"))
                        self.emit("sdiv", "r0", "r4", "r0")
                    case "==":
                        self.emit("pop", regset("r4"))
                        self.emit("cmp", "r4", "r0")
                        self.emit("moveq", "r0", 1)
                        self.emit("movne", "r0", 0)
                    case "!=":
                        self.emit("pop", regset("r4"))
                        self.emit("cmp", "r4", "r0")
                        self.emit("moveq", "r0", 0)
                        self.emit("movne", "r0", 1)
                    case "<":
                        self.emit("pop", regset("r4"))
                        self.emit("cmp", "r4", "r0")
                        self.emit("movlt", "r0", 1)
                        self.emit("movge", "r0", 0)
                    case ">":
                        self.emit("pop", regset("r4"))
                        self.emit("cmp", "r4", "r0")
                        self.emit("movgt", "r0", 1)
                        self.emit("movle", "r0", 0)
                    case "<=":
                        self.emit("pop", regset("r4"))
                        self.emit("cmp", "r4", "r0")
                        self.emit("movle", "r0", 1)
                        self.emit("movgt", "r0", 0)
                    case ">=":
                        self.emit("pop", regset("r4"))
                        self.emit("cmp", "r4", "r0")
                        self.emit("movge", "r0", 1)
                        self.emit("movlt", "r0", 0)
                    case _:
                        raise ValueError(f"unknown binary operator: {op}")
            case _:
                raise ValueError(f"unknwon expr: {expr}")

    def emit_call_expr(self, expr):
        match expr:
            case CallExpr(expr=NameExpr(name=name), args=args):
                reg_args = args[:4]
                stack_args = args[4:]
                for arg in stack_args[::-1]:
                    self.emit_expr(arg)
                    self.emit("push", regset("r0"))
                for i, arg in enumerate(reg_args[::-1]):
                    self.emit_expr(arg)
                    reg = 3 - i
                    if reg > 0:
                        self.emit("mov", f"r{reg}", "r0")
                self.emit("bl", f"{name}(PLT)")
                self.emit("add", "sp", len(stack_args)*4)
            case _:
                raise NotImplementedError
