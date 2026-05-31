"""
point.project.creator
~~~~~~~~~~~~~~~~~~~~~

Project generation utilities.

Responsibilities
----------------

- create Point projects
- create lessons
- install project templates
- generate initial configuration

Point 1.0 Project Layout
------------------------

project/
├── lessons/
├── docs/
├── assets/
├── components/
├── glossary/
├── graph/
├── paths/
├── .github/
│   └── workflows/
├── package.json
└── point.toml
"""

from pathlib import Path
from shutil import copyfile

from point.project.manager import (
    ProjectManager,
)


def create_lesson(
    name: str,
) -> Path:
    """
    Create a lesson file.
    """

    project = ProjectManager()

    template_path = Path(__file__).parent.parent / "templates" / "lesson.point"

    template = template_path.read_text(encoding="utf-8")

    content = template.replace(
        "{{title}}",
        name.replace("-", " ").title(),
    )

    output_path = project.lessons_dir / f"{name}.point"

    output_path.write_text(
        content,
        encoding="utf-8",
    )

    return output_path


def create_project(
    root: Path,
) -> None:
    """
    Create Point project structure.
    """

    #
    # Core
    #

    directories = [
        "lessons",
        "docs",
        #
        # Assets
        #
        "assets",
        "components",
        #
        # Generated Content
        #
        "glossary",
        "graph",
        "paths",
    ]

    for directory in directories:
        (root / directory).mkdir(
            parents=True,
            exist_ok=True,
        )

    #
    # package.json
    #

    package_template = (
        Path(__file__).parent.parent / "templates" / "package.json"
    )

    copyfile(
        package_template,
        root / "package.json",
    )

    #
    # point.toml
    #

    point_toml = """
title = "My Point Course"
author = ""
version = "1.0.0"
description = ""

lessons_dir = "lessons"
docs_dir = "docs"

assets_dir = "assets"
components_dir = "components"

glossary_dir = "glossary"
graph_dir = "graph"
paths_dir = "paths"

[theme]
accent_color = "#646cff"
dark_mode = true

[build]
glossary = true
knowledge_graph = true
learning_paths = true
components = true
versioning = true
"""

    (root / "point.toml").write_text(
        point_toml.strip() + "\n",
        encoding="utf-8",
    )

    #
    # Welcome Lesson
    #

    lesson_template = (
        Path(__file__).parent.parent / "templates" / "lesson.point"
    )

    lesson = lesson_template.read_text(encoding="utf-8")

    (root / "lessons" / "welcome.point").write_text(
        lesson.replace(
            "{{title}}",
            "Welcome",
        ),
        encoding="utf-8",
    )
