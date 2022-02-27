.PHONY: antlr4
antlr4: simplec/parser/SimpleCLexer.py simplec/parser/SimpleCParser.py simplec/parser/SimpleCVisitor.py

simplec/parser/SimpleCLexer.py: SimpleC.g4
	antlr4 -Dlanguage=Python3 -visitor -no-listener -o simplec/parser $<

simplec/parser/SimpleCParser.py: SimpleC.g4
	antlr4 -Dlanguage=Python3 -visitor -no-listener -o simplec/parser $<

simplec/parser/SimpleCVisitor.py: SimpleC.g4
	antlr4 -Dlanguage=Python3 -visitor -no-listener -o simplec/parser $<


.PHONY: test
test:
	poetry run pytest .
