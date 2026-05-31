"""
point.cli.main
~~~~~~~~~~~~~~

Command Line Interface for Point.

Point is an educational authoring language
and documentation generation system.

Responsibilities
----------------

- project management
- lesson creation
- compilation
- validation
- documentation generation
- vitepress integration

Examples
--------

Initialize project:

    point init my-course

Create lesson:

    point create lesson intro

Build lesson:

    point build lessons/intro.point

Build entire project:

    point build-all

Run development server:

    point serve

Build production site:

    point package
"""

import subprocess
from pathlib import Path

import typer
from rich import print

from point.builders.glossary import (
    GlossaryBuilder,
)
from point.builders.paths import (
    PathBuilder,
)
from point.builders.snippets import (
    SnippetBuilder,
)
from point.compiler.pipeline import (
    compile_file,
)
from point.parser.parser import (
    Parser,
)
from point.project.cleaner import (
    clean_docs,
)
from point.project.creator import (
    create_lesson,
    create_project,
)
from point.project.manager import (
    ProjectManager,
)
from point.project.learning_path import (
    resolve_learning_path,
)
from point.tokenizer.tokenizer import (
    Tokenizer,
)
from point.validators.validator import (
    Validator,
)
from point.vitepress.generator import (
    generate_config,
)

app = typer.Typer(
    name="point",
    help="Educational authoring toolkit",
    no_args_is_help=True,
)


# ============================================================
# Helpers
# ============================================================


def parse_file(
    source_path: Path,
):
    """
    Parse Point file into AST.
    """

    content = source_path.read_text(
        encoding="utf-8",
    )

    tokens = Tokenizer().tokenize(content)

    return Parser().parse(tokens)


def load_lessons():
    """
    Load lessons included in the
    configured learning path.
    """

    project = ProjectManager()

    lessons = []

    for file in resolve_learning_path(
        project,
    ):
        lessons.append(
            parse_file(file),
        )

    return lessons

# ============================================================
# Project Commands
# ============================================================


@app.command()
@app.command()
def init(
    name: str,
):
    """
    Create a new Point project.
    """

    project_dir = Path(name)

    if project_dir.exists():
        print(f"[red]Project '{name}' already exists[/red]")

        raise typer.Exit(code=1)

    create_project(
        project_dir,
    )

    generate_config(
        title=name.replace("-", " ").title(),
        docs_dir=project_dir / "docs",
    )

    print(f"[green]Initialized:[/green] {project_dir}")


@app.command()
def create(
    type: str,
    name: str,
):
    """
    Create project resource.
    """

    if type != "lesson":
        print("[red]Unsupported resource[/red]")

        raise typer.Exit(code=1)

    create_lesson(name)

    print(f"[green]Created lesson:[/green] {name}")


# ============================================================
# Build Commands
# ============================================================


@app.command()
def build(
    source: str,
    output: str | None = None,
):
    """
    Build single lesson.
    """

    source_path = Path(source)

    if not source_path.exists():
        print("[red]Source file not found[/red]")

        raise typer.Exit(code=1)

    if output:
        output_path = Path(output)

    else:
        project = ProjectManager()

        if source_path.stem == "welcome":
            output_path = project.docs_dir / "index.md"
        else:
            output_path = project.docs_dir / f"{source_path.stem}.md"

    compile_file(
        source_path,
        output_path,
    )

    print(f"[green]Built:[/green] {output_path}")


@app.command("build-all")
def build_all():
    """
    Build entire project.
    """

    project = ProjectManager()

    clean_docs()

    files = resolve_learning_path(
        project,
    )

    if not files:
        print("[yellow]No lessons found[/yellow]")

        return

    for file in files:
        relative = file.relative_to(project.lessons_dir)

        if file.stem == "welcome":
            output = project.docs_dir / "index.md"
        else:
            output = project.docs_dir / relative.with_suffix(".md")

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        compile_file(
            file,
            output,
        )

        print(f"[green]Built:[/green] {output}")

    print("[cyan]Generating educational resources...[/cyan]")

    lessons = load_lessons()

    GlossaryBuilder().build(
        lessons,
        project.docs_dir / "glossary",
    )

    #    GraphBuilder().build(
    #        lessons,
    #        project.docs_dir / "graph",
    #    )

    PathBuilder().build(
        lessons,
        project.docs_dir / "paths",
    )

    SnippetBuilder().build(
        lessons,
        project.docs_dir / "snippets",
    )

    generate_config(
        title=project.config.title,
        docs_dir=project.docs_dir,
        base=(
            f"/{project.root.name}/" if project.config.github_pages else "/"
        ),
    )

    print("[cyan]Installing frontend dependencies...[/cyan]")

    subprocess.run(
        ["npm", "install"],
        cwd=str(project.root),
        check=True,
    )

    print("[bold green]Build completed successfully[/bold green]")


# ============================================================
# Validation
# ============================================================


@app.command()
def validate(
    source: str,
):
    """
    Validate lesson.
    """

    lesson = parse_file(Path(source))

    errors = Validator().validate(lesson)

    if not errors:
        print("[green]Validation passed[/green]")

        return

    print("[red]Validation failed[/red]")

    for error in errors:
        print(f"• {error}")

    raise typer.Exit(code=1)


# ============================================================
# Maintenance
# ============================================================


@app.command()
def clean():
    """
    Remove generated files.
    """

    clean_docs()

    print("[green]Cleaned generated files[/green]")


# ============================================================
# VitePress
# ============================================================


@app.command()
def serve():
    """
    Start development server.
    """

    project = ProjectManager()

    try:
        result = subprocess.run(
            ["npm", "run", "docs:dev"],
            cwd=str(project.root),
        )

        #
        # VitePress dev server starts correctly
        # on some systems but exits with code 1.
        #
        # Only treat codes >1 as failures.
        #

        if result.returncode > 1:
            print(
                f"[red]Development server failed "
                f"(exit code {result.returncode})[/red]"
            )

            raise typer.Exit(
                code=result.returncode,
            )

    except FileNotFoundError:
        print("[red]npm is not installed or not available in PATH[/red]")

        raise typer.Exit(code=1)

    except KeyboardInterrupt:
        print("\n[cyan]Server stopped[/cyan]")

        raise typer.Exit(code=0)


@app.command()
def package():
    """
    Create production build.
    """

    project = ProjectManager()

    try:
        subprocess.run(
            ["npm", "run", "docs:build"],
            cwd=str(project.root),
            check=True,
        )

    except FileNotFoundError:
        print("[red]npm is not installed or not available in PATH[/red]")

        raise typer.Exit(code=1)

    except subprocess.CalledProcessError as error:
        print(
            f"[red]Production build failed "
            f"(exit code {error.returncode})[/red]"
        )

        raise typer.Exit(
            code=error.returncode,
        )

    print("[green]Production build completed[/green]")


@app.command()
def preview():
    """
    Preview production build.
    """

    project = ProjectManager()

    try:
        subprocess.run(
            ["npm", "run", "docs:preview"],
            cwd=str(project.root),
            check=True,
        )

    except FileNotFoundError:
        print("[red]npm is not installed or not available in PATH[/red]")

        raise typer.Exit(code=1)

    except subprocess.CalledProcessError as error:
        print(f"[red]Preview failed (exit code {error.returncode})[/red]")

        raise typer.Exit(
            code=error.returncode,
        )

    except KeyboardInterrupt:
        print("\n[cyan]Preview stopped[/cyan]")

        raise typer.Exit(code=0)


# ============================================================
# Information
# ============================================================


@app.command()
def info():
    """
    Display project information.
    """

    project = ProjectManager()

    lessons = scan_lessons(project.lessons_dir)

    print(f"[cyan]Project:[/cyan] {project.config.title}")

    print(f"[cyan]Version:[/cyan] {project.config.version}")

    print(f"[cyan]Lessons:[/cyan] {len(lessons)}")

    print(f"[cyan]Root:[/cyan] {project.root}")


if __name__ == "__main__":
    app()
