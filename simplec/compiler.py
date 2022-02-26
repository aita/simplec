from .syntax import (
    Expr,
    Paren,
    Number,
    Unary,
    Binary,
    Name,
    Return,
)


def emit(mnemonic, *operands):
    print(f"\t{mnemonic}\t{', '.join(operands)}")


class Compiler:
    def compile(self, program, names):
        self.names = names
        frame_size = 4
        if names:
            _, max_offset = names[-1]
            frame_size = max_offset

        print(".globl main")
        print("main:")
        emit("push", "{fp, lr}")
        emit("add", "fp", "sp", "#4")
        emit("sub", "sp", f"#{frame_size}")
        for stmt in program:
            self.compile_statement(stmt)
        print("L_return:")
        emit("sub", "sp", "fp", "#4")
        emit("pop", "{fp, pc}")

    def compile_statement(self, stmt):
        match stmt:
            case Expr() as expr:
                self.compile_expression(expr)
            case Return(expression=None):
                emit("b", "L_return")
            case Return(expression=expr):
                self.compile_expression(expr)
                emit("pop", "{r0}")
                emit("b", "L_return")
            case _:
                raise ValueError(f"unknown statement: {stmt}")

    def compile_expression(self, expr):
        match expr:
            case Name(offset=offset, is_lvar=False):
                emit("ldr", "r0", f"[fp, #{-offset}]")
                emit("push", "{r0}")
            case Number(literal=literal):
                emit("mov", "r0", f"#{literal}")
                emit("push", "{r0}")
            case Paren(expression=expression):
                return self.compile_expression(expression)
            case Unary(operator=op, operand=operand):
                match op:
                    case "+":
                        self.compile_expression(operand)
                    case "-":
                        self.compile_expression(operand)
                        emit("pop", "{r0}")
                        emit("neg", "r0")
                        emit("push", "r0")
                    case _:
                        raise ValueError(f"unknown unary operator: {op}")
            case Binary(operator="=", left=left, right=right):
                if not left.is_lvar:
                    raise ValueError("LHS is not lvar")
                right = self.compile_expression(right)
                emit("pop", "{r0}")
                emit("str", "r0", f"[fp, #{-left.offset}]")
                emit("push", "{r0}")
            case Binary(operator=op, left=left, right=right):
                left = self.compile_expression(left)
                right = self.compile_expression(right)
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
