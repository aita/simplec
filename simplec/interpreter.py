from .syntax import (
    Paren,
    Number,
    Unary,
    Binary,
    Expr,
    Name,
)


class Interpreter:
    def __init__(self):
        self.vars = {}

    def interpret(self, program):
        result = 0
        for stmt in program:
            result = self.interpret_statement(stmt)
        return result

    def interpret_statement(self, stmt):
        match stmt:
            case Expr() as expr:
                return self.interpret_expression(expr)

    def interpret_expression(self, expr):
        match expr:
            case Number(literal=literal):
                return int(literal)
            case Name(name=name):
                if name in self.vars:
                    return self.vars[name]
                else:
                    raise ValueError(f"undefined variable: {name}")
            case Paren(expression=expression):
                return self.interpret_expression(expression)
            case Unary(operator=op, operand=operand):
                match op:
                    case "+":
                        return self.interpret_expression(operand)
                    case "-":
                        return self.interpret_expression(operand)
                    case _:
                        raise ValueError(f"unknown unary operator: {op}")
            case Binary(operator=op, left=left, right=right):
                if op == "=":
                    if isinstance(left, Name):
                        right = self.interpret_expression(right)
                        self.vars[left.name] = right
                        return right
                    else:
                        raise ValueError("The left expression is not assignable")
                else:
                    left = self.interpret_expression(left)
                    right = self.interpret_expression(right)
                    match op:
                        case "+":
                            return left + right
                        case "-":
                            return left - right
                        case "*":
                            return left * right
                        case "/":
                            return left // right
                        case "==":
                            return int(left == right)
                        case "!=":
                            return int(left != right)
                        case "<":
                            return int(left < right)
                        case ">":
                            return int(left > right)
                        case "<=":
                            return int(left <= right)
                        case ">=":
                            return int(left >= right)
                        case _:
                            raise ValueError(f"unknown binary operator: {op}")
            case _:
                raise NotImplementedError
