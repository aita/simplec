# Generated from SimpleC.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SimpleCParser import SimpleCParser
else:
    from SimpleCParser import SimpleCParser

# This class defines a complete generic visitor for a parse tree produced by SimpleCParser.

class SimpleCVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SimpleCParser#program.
    def visitProgram(self, ctx:SimpleCParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#translationUnit.
    def visitTranslationUnit(self, ctx:SimpleCParser.TranslationUnitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#externalDeclaration.
    def visitExternalDeclaration(self, ctx:SimpleCParser.ExternalDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#functionDefinition.
    def visitFunctionDefinition(self, ctx:SimpleCParser.FunctionDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#identifierList.
    def visitIdentifierList(self, ctx:SimpleCParser.IdentifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#statementList.
    def visitStatementList(self, ctx:SimpleCParser.StatementListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#statement.
    def visitStatement(self, ctx:SimpleCParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#expressionStatement.
    def visitExpressionStatement(self, ctx:SimpleCParser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#returnStatement.
    def visitReturnStatement(self, ctx:SimpleCParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#compoundStatement.
    def visitCompoundStatement(self, ctx:SimpleCParser.CompoundStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#ifStatement.
    def visitIfStatement(self, ctx:SimpleCParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#whileStatement.
    def visitWhileStatement(self, ctx:SimpleCParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#expression.
    def visitExpression(self, ctx:SimpleCParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:SimpleCParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#postfixExpression.
    def visitPostfixExpression(self, ctx:SimpleCParser.PostfixExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#callExpression.
    def visitCallExpression(self, ctx:SimpleCParser.CallExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#argumentExpressionList.
    def visitArgumentExpressionList(self, ctx:SimpleCParser.ArgumentExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#unaryExpression.
    def visitUnaryExpression(self, ctx:SimpleCParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:SimpleCParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:SimpleCParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#relationalExpression.
    def visitRelationalExpression(self, ctx:SimpleCParser.RelationalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#equalityExpression.
    def visitEqualityExpression(self, ctx:SimpleCParser.EqualityExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SimpleCParser#assignmentExpression.
    def visitAssignmentExpression(self, ctx:SimpleCParser.AssignmentExpressionContext):
        return self.visitChildren(ctx)



del SimpleCParser