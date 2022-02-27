from .syntax import (
    BinaryExpr,
    CompoundStmt,
    Constant,
    Expr,
    FunctionDecl,
    IfStmt,
    NameExpr,
    ParenExpr,
    ReturnStmt,
    UnaryExpr,
    WhileStmt,
)


class Compiler:
    def __init__(self, output):
        self.output = output
        self.label_count = 0

    def print(self, *args):
        print(*args, file=self.output)

    def emit(self, mnemonic, *operands):
        self.print(f"\t{mnemonic}\t{', '.join(operands)}")

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
        frame_size = func.frame.size()
        self.return_label = self.gen_label("return")

        self.print(f".globl {func.name}")
        self.emit_label(func.name)
        self.emit("push", "{fp, lr}")
        self.emit("add", "fp", "sp", "#4")
        self.emit("sub", "sp", f"#{frame_size}")
        for stmt in func.body.stmts:
            self.emit_stmt(stmt)
        self.emit_label(self.return_label)
        self.emit("sub", "sp", "fp", "#4")
        self.emit("pop", "{fp, pc}")

    def emit_stmt(self, stmt):
        match stmt:
            case Expr() as expr:
                self.emit_expr(expr)
            case ReturnStmt(expr=None):
                self.emit("b", self.return_label)
            case ReturnStmt(expr=expr):
                self.emit_expr(expr)
                self.emit("pop", "{r0}")
                self.emit("b", self.return_label)
            case CompoundStmt(stmts=stmts):
                for stmt in stmts:
                    self.emit_stmt(stmt)
            case IfStmt(condition=condition, then_stmt=then_stmt, else_stmt=None):
                end_label = self.gen_label("end")
                self.emit_expr(condition)
                self.emit("pop", "{r0}")
                self.emit("cmp", "r0", "#0")
                self.emit("beq", end_label)
                self.emit_stmt(then_stmt)
                self.emit_label(end_label)
            case IfStmt(condition=condition, then_stmt=then_stmt, else_stmt=else_stmt):
                else_label = self.gen_label("else")
                end_label = self.gen_label("end")
                self.emit_expr(condition)
                self.emit("pop", "{r0}")
                self.emit("cmp", "r0", "#0")
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
                self.emit("pop", "{r0}")
                self.emit("cmp", "r0", "#0")
                self.emit("beq", end_label)
                self.emit_stmt(stmt)
                self.emit("b", begin_label)
                self.emit_label(end_label)
            case _:
                raise ValueError(f"unknown stmt: {stmt}")

    def emit_expr(self, expr):
        match expr:
            case NameExpr(offset=offset, is_lvar=False):
                self.emit("ldr", "r0", f"[fp, #{-offset}]")
                self.emit("push", "{r0}")
            case Constant(literal=literal):
                self.emit("mov", "r0", f"#{literal}")
                self.emit("push", "{r0}")
            case ParenExpr(expr=expr):
                return self.emit_expr(expr)
            case UnaryExpr(operator=op, operand=operand):
                match op:
                    case "+":
                        self.emit_expr(operand)
                    case "-":
                        self.emit_expr(operand)
                        self.emit("pop", "{r0}")
                        self.emit("neg", "r0")
                        self.emit("push", "r0")
                    case _:
                        raise ValueError(f"unknown unary operator: {op}")
            case BinaryExpr(operator="=", left=left, right=right):
                if not left.is_lvar:
                    raise ValueError("LHS is not lvar")
                right = self.emit_expr(right)
                self.emit("pop", "{r0}")
                self.emit("str", "r0", f"[fp, #{-left.offset}]")
                self.emit("push", "{r0}")
            case BinaryExpr(operator=op, left=left, right=right):
                left = self.emit_expr(left)
                right = self.emit_expr(right)
                match op:
                    case "+":
                        self.emit("pop", "{r0, r1}")
                        self.emit("add", "r0", "r1", "r0")
                        self.emit("push", "{r0}")
                    case "-":
                        self.emit("pop", "{r0, r1}")
                        self.emit("sub", "r0", "r1", "r0")
                        self.emit("push", "{r0}")
                    case "*":
                        self.emit("pop", "{r0, r1}")
                        self.emit("mul", "r0", "r1", "r0")
                        self.emit("push", "{r0}")
                    case "/":
                        self.emit("pop", "{r0, r1}")
                        self.emit("sdiv", "r0", "r1", "r0")
                        self.emit("push", "{r0}")
                    case "==":
                        self.emit("pop", "{r0, r1}")
                        self.emit("cmp", "r1", "r0")
                        self.emit("moveq", "r0", "#1")
                        self.emit("movne", "r0", "#0")
                        self.emit("push", "{r0}")
                    case "!=":
                        self.emit("pop", "{r0, r1}")
                        self.emit("cmp", "r1", "r0")
                        self.emit("moveq", "r0", "#0")
                        self.emit("movne", "r0", "#1")
                        self.emit("push", "{r0}")
                    case "<":
                        self.emit("pop", "{r0, r1}")
                        self.emit("cmp", "r1", "r0")
                        self.emit("movlt", "r0", "#1")
                        self.emit("movge", "r0", "#0")
                        self.emit("push", "{r0}")
                    case ">":
                        self.emit("pop", "{r0, r1}")
                        self.emit("cmp", "r1", "r0")
                        self.emit("movgt", "r0", "#1")
                        self.emit("movle", "r0", "#0")
                        self.emit("push", "{r0}")
                    case "<=":
                        self.emit("pop", "{r0, r1}")
                        self.emit("cmp", "r1", "r0")
                        self.emit("movle", "r0", "#1")
                        self.emit("movgt", "r0", "#0")
                        self.emit("push", "{r0}")
                    case ">=":
                        self.emit("pop", "{r0, r1}")
                        self.emit("cmp", "r1", "r0")
                        self.emit("movge", "r0", "#1")
                        self.emit("movlt", "r0", "#0")
                        self.emit("push", "{r0}")
                    case _:
                        raise ValueError(f"unknown binary operator: {op}")
            case _:
                raise ValueError(f"unknwon expr: {expr}")
