import os
import subprocess
from functools import cache
from pathlib import Path

import typer

app = typer.Typer(help="Plyaska Backend CLI - Auto generate __init__.py files")

@cache
@app.command()
def run_mkinit_for_all(base_dir: str):
    """To generate automatically the import of modules in this directory and submarines.
    :param base_dir: The path to the Directory with the modules
    """
    for root, dirs, files in os.walk(base_dir):
        if "__pycache__" in root:
            continue
        if any(f.endswith(".py") for f in files):
            print(f"🏗️ Generating __init__.py in {root}")
            subprocess.run(
                ["mkinit", root, "--noattrs", "-i"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )


if __name__ == "__main__":
    path = Path(__file__).parent.parent.parent.parent
    run_mkinit_for_all(path.__str__())
