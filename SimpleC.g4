grammar SimpleC;

If: 'if';
Return: 'return';
While: 'while';

LBrace: '{';
RBrace: '}';
LParen: '(';
RParen: ')';

Less: '<';
LessEqual: '<=';
Greater: '>';
GreaterEqual: '>=';

Plus: '+';
Minus: '-';
Star: '*';
Div: '/';

Question: '?';
Colon: ':';
Semi: ';';
Comma: ',';

Assign: '=';

Equal: '==';
NotEqual: '!=';

Identifier: Letter (Letter | Digit)*;

fragment Letter: [a-zA-Z_];

fragment Digit: [0-9];

fragment NonZeroDigit: [1-9];

Constant: NonZeroDigit Digit* | '0';

Whitespace: [ \t]+ -> skip;

Newline: ('\r' '\n'? | '\n') -> skip;

program: statementList;

statementList: statement*;

statement:
	expressionStatement
	| returnStatement
	| compoundStatement
	| ifStatement
	| whileStatement;

expressionStatement: expr = expression Semi;

returnStatement: 'return' expr = expression Semi;

compoundStatement: '{' stmts = statementList '}';

ifStatement:
	'if' '(' expr = expression ')' then_stmt = statement (
		'else' else_stmt = statement
	)?;

whileStatement:
	'while' '(' expr = expression ')' stmt = statement;

expression: assignmentExpression;

primaryExpression:
	ident = Identifier
	| constant = Constant
	| '(' expr = expression ')';

unaryExpression: op = ('+' | '-')? primaryExpression;

multiplicativeExpression:
	left = unaryExpression (
		op = ('*' | '/') right = multiplicativeExpression
	)?;

additiveExpression:
	left = multiplicativeExpression (
		op = ('+' | '-') right = multiplicativeExpression
	)?;

relationalExpression:
	left = additiveExpression (
		op = ('<' | '>' | '<=' | '>=') right = additiveExpression
	)?;

equalityExpression:
	left = relationalExpression (
		op = ('==' | '!=') right = relationalExpression
	)?;

assignmentExpression:
	expr = equalityExpression
	| left = unaryExpression op = '=' right = assignmentExpression;
