"""
point.project.cleaner
~~~~~~~~~~~~~~~~~~~~~

Project cleanup utilities.

Responsibilities
----------------

Remove generated Point artifacts while preserving
source content and project configuration.

Generated Content
-----------------

- markdown files
- glossary files
- graph files
- learning path files

Preserved Content
-----------------

- lessons/
- assets/
- components/
- point.toml
- package.json
- .vitepress/
"""

from shutil import rmtree

from point.project.manager import (
    ProjectManager,
)


def clean_docs() -> bool:
    """
    Clean generated project output.

    Preserves
    ---------
    docs/index.md
    docs/.vitepress/

    Removes
    --------
    All generated documentation artifacts.
    """

    project = ProjectManager()

    if not project.docs_dir.exists():
        return True

    preserved = {
        "index.md",
        ".vitepress",
    }

    for item in project.docs_dir.iterdir():

        if item.name in preserved:
            continue

        if item.is_dir():
            rmtree(item)

        else:
            item.unlink(
                missing_ok=True,
            )

    #
    # Remove empty directories
    # left behind by future generators.
    #

    for directory in sorted(
        project.docs_dir.rglob("*"),
        key=lambda p: len(p.parts),
        reverse=True,
    ):
        if (
            directory.is_dir()
            and directory.name != ".vitepress"
            and not any(directory.iterdir())
        ):
            directory.rmdir()

    return True
