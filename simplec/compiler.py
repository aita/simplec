from .syntax import (
    Expr,
    ParenExpr,
    NumberExpr,
    UnaryExpr,
    BinaryExpr,
    NameExpr,
    ReturnStmt,
    IfStmt,
    CompoundStmt,
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

    def compile(self, program, names):
        self.names = names
        frame_size = 4
        if names:
            _, max_offset = names[-1]
            frame_size = max_offset

        print(".globl main")
        emit_label("main")
        emit("push", "{fp, lr}")
        emit("add", "fp", "sp", "#4")
        emit("sub", "sp", f"#{frame_size}")
        for stmt in program:
            self.emit_statement(stmt)
        emit_label("L_return")
        emit("sub", "sp", "fp", "#4")
        emit("pop", "{fp, pc}")

    def emit_statement(self, stmt):
        match stmt:
            case Expr() as expr:
                self.emit_expression(expr)
            case CompoundStmt(statements=stmts):
                for stmt in stmts:
                    self.emit_statement(stmt)
            case IfStmt(condition=condition, then_statement=then_stmt, else_statement=None):
                end_label = self.gen_label("end")
                self.emit_expression(condition)
                emit("cmp", "r0", "#0")
                emit("beq", end_label)
                self.emit_statement(then_stmt)
                emit_label(end_label)
            case IfStmt(condition=condition, then_statement=then_stmt, else_statement=else_stmt):
                else_label = self.gen_label("else")
                end_label = self.gen_label("end")
                self.emit_expression(condition)
                emit("cmp", "r0", "#0")
                emit("beq", else_label)
                self.emit_statement(then_stmt)
                emit("b", end_label)
                emit_label(else_label)
                self.emit_statement(else_stmt)
                emit_label(end_label)                
            case ReturnStmt(expression=None):
                emit("b", "L_return")
            case ReturnStmt(expression=expr):
                self.emit_expression(expr)
                emit("pop", "{r0}")
                emit("b", "L_return")
            case _:
                raise ValueError(f"unknown statement: {stmt}")

    def emit_expression(self, expr):
        match expr:
            case NameExpr(offset=offset, is_lvar=False):
                emit("ldr", "r0", f"[fp, #{-offset}]")
                emit("push", "{r0}")
            case NumberExpr(literal=literal):
                emit("mov", "r0", f"#{literal}")
                emit("push", "{r0}")
            case ParenExpr(expression=expression):
                return self.emit_expression(expression)
            case UnaryExpr(operator=op, operand=operand):
                match op:
                    case "+":
                        self.emit_expression(operand)
                    case "-":
                        self.emit_expression(operand)
                        emit("pop", "{r0}")
                        emit("neg", "r0")
                        emit("push", "r0")
                    case _:
                        raise ValueError(f"unknown unary operator: {op}")
            case BinaryExpr(operator="=", left=left, right=right):
                if not left.is_lvar:
                    raise ValueError("LHS is not lvar")
                right = self.emit_expression(right)
                emit("pop", "{r0}")
                emit("str", "r0", f"[fp, #{-left.offset}]")
                emit("push", "{r0}")
            case BinaryExpr(operator=op, left=left, right=right):
                left = self.emit_expression(left)
                right = self.emit_expression(right)
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
                raise ValueError(f"unknwon expression: {expr}")
