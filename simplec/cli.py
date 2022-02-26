import click

from .compiler import Compiler
from .parser import parse
from .interpreter import Interpreter


@click.command()
@click.argument("filename")
def compiler(filename):
    with open(filename) as fp:
        program, names = parse(fp.read())
        compiler = Compiler()
        compiler.compile(program, names)


@click.command()
@click.argument("filename")
def interpreter(filename):
    with open(filename) as fp:
        program, names = parse(fp.read())
        interpreter = Interpreter()
        result = interpreter.interpret(program)
        print(result)


if __name__ == "__main__":
    cli()
