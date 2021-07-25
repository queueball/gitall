#!/usr/local/bin/python3
import json
import pathlib
import subprocess

import click


CHECKS = (
    b"",
    b"## \x1b[32mmaster\x1b[m\n",
    b"## \x1b[32mmaster\x1b[m...\x1b[31morigin/master\x1b[m\n",
    b"## \x1b[32mmain\x1b[m\n",
    b"## \x1b[32mmain\x1b[m...\x1b[31morigin/main\x1b[m\n",
)


@click.command()
@click.argument("params", nargs=-1)
def controller(params):
    if not params:
        params = ["stat"]
    paths = []
    try:
        with open(pathlib.Path("~/.gitall.json").expanduser()) as f:
            paths = json.load(f)["paths"]
    finally:
        pass
    tech, home = (pathlib.Path(a).expanduser() for a in paths)
    dirs = list(tech.iterdir()) + [home]
    first = True
    for dir_ in (d for d in sorted(dirs) if (d / ".git").exists()):
        params_ = [f'"{i}"' if " " in i else i for i in params]
        cmd = " ".join(["git"] + params_)
        try:
            result = subprocess.check_output(cmd, cwd=dir_, shell=True)
            if result not in CHECKS:
                click.echo(("" if first else "\n") + f">>> { cmd } { dir_ }")
                click.echo(result[:-1].decode())
                first = False
        except Exception as e:
            click.echo(e)


if __name__ == "__main__":
    controller()
