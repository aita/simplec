from .syntax import (
    Expr,
    ParenExpr,
    Constant,
    UnaryExpr,
    BinaryExpr,
    NameExpr,
    ReturnStmt,
    IfStmt,
    CompoundStmt,
    WhileStmt,
)


def emit(mnemonic, *operands):
    print(f"\t{mnemonic}\t{', '.join(operands)}")


def emit_label(label):
    print(f"{label}:")


class Compiler:
    def __init__(self):
        self.label_count = 0

    def gen_label(self, name):
        label = f"L_{name}_{self.label_count}"
        self.label_count += 1
        return label

    def compile(self, program, frame):
        frame_size = frame.size()

        print(".globl main")
        emit_label("main")
        emit("push", "{fp, lr}")
        emit("add", "fp", "sp", "#4")
        emit("sub", "sp", f"#{frame_size}")
        for stmt in program:
            self.emit_stmt(stmt)
        emit_label("L_return")
        emit("sub", "sp", "fp", "#4")
        emit("pop", "{fp, pc}")

    def emit_stmt(self, stmt):
        match stmt:
            case Expr() as expr:
                self.emit_expr(expr)
            case ReturnStmt(expr=None):
                emit("b", "L_return")
            case ReturnStmt(expr=expr):
                self.emit_expr(expr)
                emit("pop", "{r0}")
                emit("b", "L_return")
            case CompoundStmt(stmts=stmts):
                for stmt in stmts:
                    self.emit_stmt(stmt)
            case IfStmt(condition=condition, then_stmt=then_stmt, else_stmt=None):
                end_label = self.gen_label("end")
                self.emit_expr(condition)
                emit("pop", "{r0}")
                emit("cmp", "r0", "#0")
                emit("beq", end_label)
                self.emit_stmt(then_stmt)
                emit_label(end_label)
            case IfStmt(condition=condition, then_stmt=then_stmt, else_stmt=else_stmt):
                else_label = self.gen_label("else")
                end_label = self.gen_label("end")
                self.emit_expr(condition)
                emit("pop", "{r0}")
                emit("cmp", "r0", "#0")
                emit("beq", else_label)
                self.emit_stmt(then_stmt)
                emit("b", end_label)
                emit_label(else_label)
                self.emit_stmt(else_stmt)
                emit_label(end_label)           
            case WhileStmt(condition=condition, stmt=stmt):
                begin_label = self.gen_label("begin")
                end_label = self.gen_label("end")
                emit_label(begin_label)                 
                self.emit_expr(condition)
                emit("pop", "{r0}")
                emit("cmp", "r0", "#0")
                emit("beq", end_label)
                self.emit_stmt(stmt)
                emit("b", begin_label)
                emit_label(end_label)                 
            case _:
                raise ValueError(f"unknown stmt: {stmt}")

    def emit_expr(self, expr):
        match expr:
            case NameExpr(offset=offset, is_lvar=False):
                emit("ldr", "r0", f"[fp, #{-offset}]")
                emit("push", "{r0}")
            case Constant(literal=literal):
                emit("mov", "r0", f"#{literal}")
                emit("push", "{r0}")
            case ParenExpr(expr=expr):
                return self.emit_expr(expr)
            case UnaryExpr(operator=op, operand=operand):
                match op:
                    case "+":
                        self.emit_expr(operand)
                    case "-":
                        self.emit_expr(operand)
                        emit("pop", "{r0}")
                        emit("neg", "r0")
                        emit("push", "r0")
                    case _:
                        raise ValueError(f"unknown unary operator: {op}")
            case BinaryExpr(operator="=", left=left, right=right):
                if not left.is_lvar:
                    raise ValueError("LHS is not lvar")
                right = self.emit_expr(right)
                emit("pop", "{r0}")
                emit("str", "r0", f"[fp, #{-left.offset}]")
                emit("push", "{r0}")
            case BinaryExpr(operator=op, left=left, right=right):
                left = self.emit_expr(left)
                right = self.emit_expr(right)
                match op:
                    case "+":
                        emit("pop", "{r0, r1}")
                        emit("add", "r0", "r1", "r0")
                        emit("push", "{r0}")
                    case "-":
                        emit("pop", "{r0, r1}")
                        emit("sub", "r0", "r1", "r0")
                        emit("push", "{r0}")
                    case "*":
                        emit("pop", "{r0, r1}")
                        emit("mul", "r0", "r1", "r0")
                        emit("push", "{r0}")
                    case "/":
                        emit("pop", "{r0, r1}")
                        emit("sdiv", "r0", "r1", "r0")
                        emit("push", "{r0}")
                    case "==":
                        emit("pop", "{r0, r1}")
                        emit("cmp", "r1", "r0")
                        emit("moveq", "r0", "#1")
                        emit("movne", "r0", "#0")
                        emit("push", "{r0}")
                    case "!=":
                        emit("pop", "{r0, r1}")
                        emit("cmp", "r1", "r0")
                        emit("moveq", "r0", "#0")
                        emit("movne", "r0", "#1")
                        emit("push", "{r0}")
                    case "<":
                        emit("pop", "{r0, r1}")
                        emit("cmp", "r1", "r0")
                        emit("movlt", "r0", "#1")
                        emit("movge", "r0", "#0")
                        emit("push", "{r0}")
                    case ">":
                        emit("pop", "{r0, r1}")
                        emit("cmp", "r1", "r0")
                        emit("movgt", "r0", "#1")
                        emit("movle", "r0", "#0")
                        emit("push", "{r0}")
                    case "<=":
                        emit("pop", "{r0, r1}")
                        emit("cmp", "r1", "r0")
                        emit("movle", "r0", "#1")
                        emit("movgt", "r0", "#0")
                        emit("push", "{r0}")
                    case ">=":
                        emit("pop", "{r0, r1}")
                        emit("cmp", "r1", "r0")
                        emit("movge", "r0", "#1")
                        emit("movlt", "r0", "#0")
                        emit("push", "{r0}")
                    case _:
                        raise ValueError(f"unknown binary operator: {op}")
            case _:
                raise ValueError(f"unknwon expr: {expr}")
