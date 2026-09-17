import posixpath
from pathlib import Path

import typer
from inflection import camelize, underscore

app = typer.Typer(help="Plyaska Backend CLI - Generate files by templates")


def generate_by_template(template_folder: str, name: str, _type: str):
    if _type == "models":
        to_write = f"./src/{_type}/{name}.py"
    elif _type == "controllers":
        to_write = f"./src/{_type}/{name}_crud.py"
    elif _type == "tests":
        to_write = f"./tests/controllers/test_{name}s.py"
    else:
        to_write = f"./src/{_type}/{name}.py"
    with open(f"{template_folder}/{_type}.txt", "rt") as f:
        text = f.read().format(name=name, class_name=camelize(name))
        Path(to_write).write_text(text)
        typer.echo(f"🧱 Created a file of type {_type} in {to_write}")


@app.command(name="generate by template")
def generate(
    name: str = typer.Argument(..., help="Write in snake case"),
    exclude: str = typer.Option(
        "",
        "--exclude",
        "-e",
        help="Comma-separated list of types to exclude. Available types: models, repositories, services, controllers, tests",
    ),
):
    """Generate a file blank with a template code."""
    templates_folder_path = f"{posixpath.dirname(__file__)}/templates"

    file_name = underscore(name)

    types = [
        "models",
        "repositories",
        "services",
        "controllers",
        "tests",
    ]

    if exclude:
        exclude_types = {etype.strip() for etype in exclude.split(",")}
        types = [t for t in types if t not in exclude_types]

    for value in types:
        generate_by_template(templates_folder_path, file_name, value)


if __name__ == "__main__":
    generate("promotion", "models,services,controllers")
