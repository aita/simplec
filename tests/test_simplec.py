import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner

from simplec import cli


def fixture_path(path):
    return str(Path(__file__).parent / path)


@pytest.mark.parametrize(
    "src,returncode",
    [
        ("fixtures/one.c", 1),
        ("fixtures/add.c", 8),
    ],
)
def test_compiler(tmpdir, src, returncode):
    runner = CliRunner()
    result = runner.invoke(cli.compiler, [fixture_path(src)])
    assert result.exit_code == 0

    asm_path = tmpdir / f"{Path(src).stem}.s"
    exe_path = tmpdir / Path(src).stem
    with open(asm_path, "w") as fp:
        fp.write(result.output)

    assert (
        subprocess.run(
            ["arm-linux-gnueabihf-gcc", str(asm_path), "-o", str(exe_path)]
        ).returncode
        == 0
    )
    result = subprocess.run(
        ["qemu-arm-static", "-L", "/usr/arm-linux-gnueabihf/", str(exe_path)],
        capture_output=True,
    )
    assert result.returncode == returncode
