# Generated from SimpleC.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SimpleCParser import SimpleCParser
else:
    from SimpleCParser import SimpleCParser

# This class defines a complete listener for a parse tree produced by SimpleCParser.
class SimpleCListener(ParseTreeListener):

    # Enter a parse tree produced by SimpleCParser#program.
    def enterProgram(self, ctx:SimpleCParser.ProgramContext):
        pass

    # Exit a parse tree produced by SimpleCParser#program.
    def exitProgram(self, ctx:SimpleCParser.ProgramContext):
        pass


    # Enter a parse tree produced by SimpleCParser#statementList.
    def enterStatementList(self, ctx:SimpleCParser.StatementListContext):
        pass

    # Exit a parse tree produced by SimpleCParser#statementList.
    def exitStatementList(self, ctx:SimpleCParser.StatementListContext):
        pass


    # Enter a parse tree produced by SimpleCParser#statement.
    def enterStatement(self, ctx:SimpleCParser.StatementContext):
        pass

    # Exit a parse tree produced by SimpleCParser#statement.
    def exitStatement(self, ctx:SimpleCParser.StatementContext):
        pass


    # Enter a parse tree produced by SimpleCParser#expressionStatement.
    def enterExpressionStatement(self, ctx:SimpleCParser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by SimpleCParser#expressionStatement.
    def exitExpressionStatement(self, ctx:SimpleCParser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by SimpleCParser#returnStatement.
    def enterReturnStatement(self, ctx:SimpleCParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by SimpleCParser#returnStatement.
    def exitReturnStatement(self, ctx:SimpleCParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by SimpleCParser#compoundStatement.
    def enterCompoundStatement(self, ctx:SimpleCParser.CompoundStatementContext):
        pass

    # Exit a parse tree produced by SimpleCParser#compoundStatement.
    def exitCompoundStatement(self, ctx:SimpleCParser.CompoundStatementContext):
        pass


    # Enter a parse tree produced by SimpleCParser#ifStatement.
    def enterIfStatement(self, ctx:SimpleCParser.IfStatementContext):
        pass

    # Exit a parse tree produced by SimpleCParser#ifStatement.
    def exitIfStatement(self, ctx:SimpleCParser.IfStatementContext):
        pass


    # Enter a parse tree produced by SimpleCParser#whileStatement.
    def enterWhileStatement(self, ctx:SimpleCParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by SimpleCParser#whileStatement.
    def exitWhileStatement(self, ctx:SimpleCParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by SimpleCParser#expression.
    def enterExpression(self, ctx:SimpleCParser.ExpressionContext):
        pass

    # Exit a parse tree produced by SimpleCParser#expression.
    def exitExpression(self, ctx:SimpleCParser.ExpressionContext):
        pass


    # Enter a parse tree produced by SimpleCParser#primaryExpression.
    def enterPrimaryExpression(self, ctx:SimpleCParser.PrimaryExpressionContext):
        pass

    # Exit a parse tree produced by SimpleCParser#primaryExpression.
    def exitPrimaryExpression(self, ctx:SimpleCParser.PrimaryExpressionContext):
        pass


    # Enter a parse tree produced by SimpleCParser#unaryExpression.
    def enterUnaryExpression(self, ctx:SimpleCParser.UnaryExpressionContext):
        pass

    # Exit a parse tree produced by SimpleCParser#unaryExpression.
    def exitUnaryExpression(self, ctx:SimpleCParser.UnaryExpressionContext):
        pass


    # Enter a parse tree produced by SimpleCParser#multiplicativeExpression.
    def enterMultiplicativeExpression(self, ctx:SimpleCParser.MultiplicativeExpressionContext):
        pass

    # Exit a parse tree produced by SimpleCParser#multiplicativeExpression.
    def exitMultiplicativeExpression(self, ctx:SimpleCParser.MultiplicativeExpressionContext):
        pass


    # Enter a parse tree produced by SimpleCParser#additiveExpression.
    def enterAdditiveExpression(self, ctx:SimpleCParser.AdditiveExpressionContext):
        pass

    # Exit a parse tree produced by SimpleCParser#additiveExpression.
    def exitAdditiveExpression(self, ctx:SimpleCParser.AdditiveExpressionContext):
        pass


    # Enter a parse tree produced by SimpleCParser#relationalExpression.
    def enterRelationalExpression(self, ctx:SimpleCParser.RelationalExpressionContext):
        pass

    # Exit a parse tree produced by SimpleCParser#relationalExpression.
    def exitRelationalExpression(self, ctx:SimpleCParser.RelationalExpressionContext):
        pass


    # Enter a parse tree produced by SimpleCParser#equalityExpression.
    def enterEqualityExpression(self, ctx:SimpleCParser.EqualityExpressionContext):
        pass

    # Exit a parse tree produced by SimpleCParser#equalityExpression.
    def exitEqualityExpression(self, ctx:SimpleCParser.EqualityExpressionContext):
        pass


    # Enter a parse tree produced by SimpleCParser#assignmentExpression.
    def enterAssignmentExpression(self, ctx:SimpleCParser.AssignmentExpressionContext):
        pass

    # Exit a parse tree produced by SimpleCParser#assignmentExpression.
    def exitAssignmentExpression(self, ctx:SimpleCParser.AssignmentExpressionContext):
        pass


