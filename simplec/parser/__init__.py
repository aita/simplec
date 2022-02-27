from ast import Constant, operator
from antlr4 import CommonTokenStream, InputStream

from .SimpleCLexer import SimpleCLexer
from .SimpleCParser import SimpleCParser
from .SimpleCVisitor import SimpleCVisitor

from ..syntax import (
    BinaryExpr,
    CompoundStmt,
    IfStmt,
    NameExpr,
    ReturnStmt,
    UnaryExpr,
    Constant,
    ParenExpr,
    WhileStmt,
    FunctionDecl,
)
from ..frame import Frame


class Visitor(SimpleCVisitor):
    def visitProgram(self, ctx: SimpleCParser.ProgramContext):
        translationUnit = ctx.translationUnit()
        if translationUnit:
            return self.visit(translationUnit)
        return []

    def visitTranslationUnit(self, ctx: SimpleCParser.TranslationUnitContext):
        return [self.visit(decl) for decl in ctx.externalDeclaration()]

    def visitFunctionDefinition(self, ctx: SimpleCParser.FunctionDefinitionContext):
        self.frame = Frame()
        return FunctionDecl(
            name=ctx.ident.text, body=self.visit(ctx.body), frame=self.frame
        )

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
        return CompoundStmt(stmts=[stmt for stmt in self.visit(ctx.stmts)])

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
            var = self.frame.get_var(name)
            if var is None:
                var = self.frame.new_var(name)
            return NameExpr(name=name, offset=var.offset)
        if ctx.constant:
            return Constant(literal=ctx.constant.text)
        if ctx.expr:
            return ParenExpr(expr=self.visit(ctx.expr))

        raise ValueError("invalid primary expression")

    def visitUnaryExpression(self, ctx: SimpleCParser.UnaryExpressionContext):
        if ctx.op:
            return UnaryExpr(
                operator=ctx.op.text, operand=self.visit(ctx.primaryExpression())
            )
        else:
            return self.visit(ctx.primaryExpression())

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