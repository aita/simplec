import click

from .compiler import Compiler
from .parser import parse


@click.command()
@click.argument("filename")
def compiler(filename):
    with open(filename) as fp:
        program, frame = parse(fp.read())
        compiler = Compiler()
        compiler.compile(program, frame)


if __name__ == "__main__":
    compiler()
