import click

import sys
from contextlib import ExitStack

from .compiler import Compiler
from .parser import parse


@click.command()
@click.argument("filename")
@click.option("--output", default=None)
def compiler(filename, output):
    with ExitStack() as stack:
        input = stack.enter_context(open(filename))
        if output:
            output = stack.enter_context(open(output))
        else:
            output = sys.stdout
        program = parse(input.read())
        compiler = Compiler(output)
        compiler.compile(program)


if __name__ == "__main__":
    compiler()
