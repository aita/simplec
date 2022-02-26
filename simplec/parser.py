import os

from ply import lex, yacc
from .syntax import (
    Name,
    Number,
    Paren,
    Unary,
    Binary,
    Return,
)


class Parser:
    def __init__(self, debug):
        self.debug = debug
        self.names = []

        try:
            modname = (
                os.path.split(os.path.splitext(__file__)[0])[1]
                + "_"
                + self.__class__.__name__
            )
        except Exception:
            modname = "parser" + "_" + self.__class__.__name__
        self.debugfile = modname + ".dbg"

        self.lex = lex.lex(module=self, debug=self.debug)
        self.yacc = yacc.yacc(module=self, debug=self.debug, debugfile=self.debugfile)

    def parse(self, s):
        return self.yacc.parse(s)

    def find_name(self, name):
        for (l_name, l_offset) in self.names:
            if l_name == name:
                return l_offset
        return None

    tokens = (
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVIDE",
        "EQUAL",
        "EQUAL_EQUAL",
        "NOT_EQUAL",
        "LESS",
        "GREATER",
        "LESS_EQUAL",
        "GREATER_EQUAL",
        "SEMICOLON",
        "LPAREN",
        "RPAREN",
        "NUMBER",
        "RETURN",
        "NAME",
    )

    keywords = {
        "return": "RETURN",
    }

    t_ignore = " \r\t"

    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_TIMES = r"\*"
    t_DIVIDE = r"/"
    t_EQUAL = r"="
    t_EQUAL_EQUAL = r"=="
    t_NOT_EQUAL = r"!="
    t_LESS = r"<"
    t_GREATER = r">"
    t_LESS_EQUAL = r"<="
    t_GREATER_EQUAL = r">="
    t_SEMICOLON = r";"
    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_RETURN = r"return"

    def t_NAME(self, t):
        r"[a-zA-Z_][a-zA-Z0-9_]*"
        if t.value in self.keywords:
            t.type = self.keywords[t.value]
        return t

    def t_NUMBER(self, t):
        r"\d+"
        t.value = int(t.value)
        return t

    def t_ignore_newline(self, t):
        r"\n+"
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print(f"Illegal character {t.value[0]!r}")
        t.lexer.skip(1)

    precedence = (
        ("right", "EQUAL"),
        ("left", "EQUAL_EQUAL", "NOT_EQUAL"),
        ("left", "LESS", "GREATER", "LESS_EQUAL", "GREATER_EQUAL"),
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE"),
    )

    def p_program(self, p):
        """
        program : statement_list
        """
        p[0] = p[1]

    def p_statement_list_null(self, p):
        """
        statement_list :
        """
        p[0] = []

    def p_statement_list_first(self, p):
        """
        statement_list : statement
        """
        p[0] = [p[1]]

    def p_statement_list_rest(self, p):
        """
        statement_list : statement_list statement
        """
        p[0] = p[1] + [p[2]]

    def p_statement(self, p):
        """
        statement : expression SEMICOLON
                  | return
        """
        p[0] = p[1]

    def p_return(self, p):
        """
        return : RETURN expression SEMICOLON
               | RETURN SEMICOLON
        """
        if len(p) == 4:
            p[0] = Return(expression=p[2])
        else:
            p[0] = Return(expression=None)

    def p_expression(self, p):
        """
        expression : binary
                | unary
                | primary
                | assign
        """
        p[0] = p[1]

    def p_assign(self, p):
        """
        assign : expression EQUAL expression
        """
        p[1].is_lvar = True
        p[0] = Binary(operator=p[2], left=p[1], right=p[3])

    def p_binary(self, p):
        """
        binary : expression PLUS expression
            | expression MINUS expression
            | expression TIMES expression
            | expression DIVIDE expression
            | expression EQUAL_EQUAL expression
            | expression NOT_EQUAL expression
            | expression LESS expression
            | expression GREATER expression
            | expression LESS_EQUAL expression
            | expression GREATER_EQUAL expression
        """
        p[0] = Binary(operator=p[2], left=p[1], right=p[3])

    def p_unary(self, p):
        """
        unary : PLUS expression
            | MINUS expression
        """
        p[0] = Unary(operator=p[1], operand=p[2])

    def p_primary_number(self, p):
        """
        primary : NUMBER
        """
        p[0] = Number(p[1])

    def p_primary_name(self, p):
        """
        primary : NAME
        """
        name = p[1]
        offset = self.find_name(name)
        if offset is None:
            if self.names:
                _, offset = self.names[-1]
            else:
                offset = 4
            offset += 4
            self.names.append((name, offset))
        p[0] = Name(name=name, offset=offset)

    def p_primary_paren(self, p):
        """
        primary : LPAREN expression RPAREN
        """
        p[0] = Paren(expression=p[2])

    def p_error(self, p):
        # Read ahead looking for a closing ';'
        while True:
            tok = self.yacc.token()
            if not tok or tok.type == "SEMICOLON":
                break
        self.yacc.errok()

        return tok


def parse(text, debug=0):
    parser = Parser(debug)
    ast = parser.parse(text)
    # if parser.error:
    #     return None
    return ast, parser.names
