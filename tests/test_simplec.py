import subprocess
import pytest
from click.testing import CliRunner

from pathlib import Path

from simplec import cli


def fixture_path(path):
    return str(Path(__file__).parent / path)


def test_one(tmpdir):
    runner = CliRunner()
    result = runner.invoke(cli.compiler, [fixture_path("fixtures/one.c")])
    assert result.exit_code == 0

    asm_path = tmpdir / "test.s"
    with open(asm_path, "w") as fp:
        fp.write(result.output)

    assert subprocess.run(["arm-linux-gnueabihf-gcc", str(asm_path)]).returncode == 0
