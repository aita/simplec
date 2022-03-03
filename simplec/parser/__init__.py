from contextlib import contextmanager

from antlr4 import CommonTokenStream, InputStream

from ..syntax import (
    BinaryExpr,
    CallExpr,
    CompoundStmt,
    Constant,
    FunctionDecl,
    IfStmt,
    NameExpr,
    ParamDecl,
    ParenExpr,
    Position,
    ReturnStmt,
    Scope,
    Symbol,
    UnaryExpr,
    WhileStmt,
)
from .SimpleCLexer import SimpleCLexer
from .SimpleCParser import SimpleCParser
from .SimpleCVisitor import SimpleCVisitor


def token_position(token):
    return Position(
        start=token.start,
        end=token.stop,
        line=token.line,
        column=token.column,
    )


class Visitor(SimpleCVisitor):
    def __init__(self):
        self.scope = Scope(parent=None)
        self.errors = []

    def error(self, message):
        self.errors.append(message)

    def new_symbol(self, ident):
        name = ident.text
        if name in self.scope.symbols:
            self.error("already declared")
        symbol = Symbol(
            name=name,
            decl=None,
            pos=token_position(ident),
        )
        self.scope.symbols[name] = symbol
        return symbol

    @contextmanager
    def set_scope(self, scope=None):
        last_scope = self.scope
        if scope is None:
            scope = Scope(parent=last_scope)
        if scope != last_scope:
            last_scope.children.append(scope)
        self.scope = scope
        yield
        self.scope = last_scope

    def visitProgram(self, ctx: SimpleCParser.ProgramContext):
        translationUnit = ctx.translationUnit()
        if translationUnit:
            return self.visit(translationUnit)
        return []

    def visitTranslationUnit(self, ctx: SimpleCParser.TranslationUnitContext):
        return [self.visit(decl) for decl in ctx.externalDeclaration()]

    def visitFunctionDefinition(self, ctx: SimpleCParser.FunctionDefinitionContext):
        with self.set_scope():
            symbol = self.new_symbol(ctx.ident)
            ctx.body.scope = self.scope
            if ctx.params:
                params = self.visit(ctx.params)
            else:
                params = []
            func = FunctionDecl(
                name=ctx.ident.text,
                params=params,
                body=self.visit(ctx.body),
                scope=self.scope,
                symbol=symbol,
            )
            symbol.decl = func
            return func

    def visitIdentifierList(self, ctx: SimpleCParser.IdentifierListContext):
        params = []
        for ident in ctx.Identifier():
            symbol = self.new_symbol(ident.symbol)
            decl = ParamDecl(
                name=ident.symbol.text,
                symbol=symbol,
            )
            symbol.decl = decl
            params.append(decl)
        return params

    def visitStatementList(self, ctx: SimpleCParser.StatementListContext):
        return [self.visit(ctx) for ctx in ctx.statement()]

    def visitExpressionStatement(self, ctx: SimpleCParser.ExpressionStatementContext):
        return self.visit(ctx.expr)

    def visitReturnStatement(self, ctx: SimpleCParser.ReturnStatementContext):
        expr = None
        if ctx.expr:
            expr = self.visit(ctx.expr)
        return ReturnStmt(expr=expr)

    def visitCompoundStatement(self, ctx: SimpleCParser.CompoundStatementContext):
        with self.set_scope(scope=getattr(ctx, "scope", None)):
            return CompoundStmt(
                stmts=self.visit(ctx.stmts),
                scope=self.scope,
            )

    def visitIfStatement(self, ctx: SimpleCParser.IfStatementContext):
        else_stmt = None
        if ctx.else_stmt:
            else_stmt = self.visit(ctx.else_stmt)
        return IfStmt(
            condition=self.visit(ctx.expr),
            then_stmt=self.visit(ctx.then_stmt),
            else_stmt=else_stmt,
        )

    def visitWhileStatement(self, ctx: SimpleCParser.WhileStatementContext):
        return WhileStmt(
            condition=self.visit(ctx.expr),
            stmt=self.visit(ctx.stmt),
        )

    def visitPrimaryExpression(self, ctx: SimpleCParser.PrimaryExpressionContext):
        if ctx.ident:
            name = ctx.ident.text
            symbol = self.scope.find_name(name)
            if symbol is None:
                symbol = self.new_symbol(ctx.ident)
                expr = NameExpr(name=name, symbol=symbol)
                symbol.decl = expr
                return expr
            else:
                return NameExpr(name=name, symbol=symbol)
        if ctx.constant:
            return Constant(literal=ctx.constant.text)
        if ctx.expr:
            return ParenExpr(expr=self.visit(ctx.expr))

        raise ValueError("invalid primary expression")

    def visitCallExpression(self, ctx: SimpleCParser.CallExpressionContext):
        expr = self.visit(ctx.primaryExpression())
        if ctx.args:
            args = self.visit(ctx.args)
        else:
            args = []
        return CallExpr(expr=expr, args=args)

    def visitArgumentExpressionList(
        self, ctx: SimpleCParser.ArgumentExpressionListContext
    ):
        return [self.visit(expr) for expr in ctx.assignmentExpression()]

    def visitUnaryExpression(self, ctx: SimpleCParser.UnaryExpressionContext):
        if ctx.op:
            return UnaryExpr(
                operator=ctx.op.text, operand=self.visit(ctx.postfixExpression())
            )
        else:
            return self.visit(ctx.postfixExpression())

    def visitMultiplicativeExpression(
        self, ctx: SimpleCParser.MultiplicativeExpressionContext
    ):
        if ctx.right:
            return BinaryExpr(
                operator=ctx.op.text,
                left=self.visit(ctx.left),
                right=self.visit(ctx.right),
            )
        else:
            return self.visit(ctx.left)

    def visitAdditiveExpression(self, ctx: SimpleCParser.AdditiveExpressionContext):
        if ctx.right:
            return BinaryExpr(
                operator=ctx.op.text,
                left=self.visit(ctx.left),
                right=self.visit(ctx.right),
            )
        else:
            return self.visit(ctx.left)

    def visitRelationalExpression(self, ctx: SimpleCParser.RelationalExpressionContext):
        if ctx.right:
            return BinaryExpr(
                operator=ctx.op.text,
                left=self.visit(ctx.left),
                right=self.visit(ctx.right),
            )
        else:
            return self.visit(ctx.left)

    def visitEqualityExpression(self, ctx: SimpleCParser.EqualityExpressionContext):
        if ctx.right:
            return BinaryExpr(
                operator=ctx.op.text,
                left=self.visit(ctx.left),
                right=self.visit(ctx.right),
            )
        else:
            return self.visit(ctx.left)

    def visitAssignmentExpression(self, ctx: SimpleCParser.AssignmentExpressionContext):
        if ctx.right:
            left = self.visit(ctx.left)
            left.is_lvar = True
            return BinaryExpr(
                operator=ctx.op.text,
                left=left,
                right=self.visit(ctx.right),
            )
        else:
            return self.visit(ctx.expr)


def parse(text):
    lexer = SimpleCLexer(InputStream(text))
    stream = CommonTokenStream(lexer)
    parser = SimpleCParser(stream)
    tree = parser.program()
    visitor = Visitor()
    return visitor.visit(tree)
