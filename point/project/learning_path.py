"""
point.project.learning_path
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Learning path resolution.

Responsibilities
----------------

Convert learning path configuration from
point.toml into an ordered sequence of
lesson files.

The learning path acts as the source of
truth for:

- build order
- sidebar order
- glossary generation
- learning paths
- snippet extraction
"""

from pathlib import Path

from point.project.manager import (
    ProjectManager,
)
from point.project.scanner import (
    scan_lessons,
)

def resolve_learning_path(
    project: ProjectManager,
) -> list[Path]:
    """
    Resolve configured lesson order.

    Returns
    -------
    list[Path]
        Ordered lesson files.

    Notes
    -----
    Falls back to filesystem scanning
    when no learning path is configured.
    """

    config = getattr(
        project.config,
        "learning_path",
        None,
    )

    if not config:
        return scan_lessons(
            project.lessons_dir,
        )

    include = config.get(
        "include",
        [],
    )

    if not include:
        return scan_lessons(
            project.lessons_dir,
        )

    files: list[Path] = []

    for entry in include:

        #
        # Root lesson
        #

        if isinstance(
            entry,
            str,
        ):
            lesson = (
                project.lessons_dir
                / f"{entry}.point"
            )

            if not lesson.exists():
                raise FileNotFoundError(
                    f"Lesson not found: {lesson}"
                )

            files.append(
                lesson,
            )

            continue

        #
        # Directory lessons
        #

        directory = entry["name"]

        for lesson_name in entry["lessons"]:

            lesson = (
                project.lessons_dir
                / directory
                / f"{lesson_name}.point"
            )

            if not lesson.exists():
                raise FileNotFoundError(
                    f"Lesson not found: {lesson}"
                )

            files.append(
                lesson,
            )

    return files
