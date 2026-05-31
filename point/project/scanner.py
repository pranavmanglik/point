"""
point.project.scanner
~~~~~~~~~~~~~~~~~~~~~

Project scanning utilities.

Responsibilities
----------------

Discover Point resources within a project.

Features
--------

- lesson discovery
- glossary discovery
- concept discovery
- path discovery
- reusable content indexing

Pipeline
--------

Project
    ↓

Scanner
    ↓

Point Sources
    ↓

Builders
"""

from pathlib import Path


def scan_lessons(
    lessons_dir: Path,
) -> list[Path]:
    """
    Scan lesson directory.

    Parameters
    ----------
    lessons_dir:
        Directory containing
        Point lesson files.

    Returns
    -------
    list[Path]
        Sorted Point source files.
    """

    files = list(lessons_dir.rglob("*.point"))

    return sorted(
        files,
        key=lambda path: path.name,
    )


def scan_directory(
    directory: Path,
    extension: str,
) -> list[Path]:
    """
    Generic directory scanner.

    Parameters
    ----------
    directory:
        Root directory.

    extension:
        File extension.

    Returns
    -------
    list[Path]
    """

    files = list(directory.rglob(f"*.{extension}"))

    return sorted(
        files,
        key=lambda path: path.name,
    )


def lesson_names(
    lessons_dir: Path,
) -> list[str]:
    """
    Return lesson names.

    Example
    -------

    intro.point

    becomes

    intro
    """

    return [file.stem for file in scan_lessons(lessons_dir)]


def lesson_map(
    lessons_dir: Path,
) -> dict[str, Path]:
    """
    Create lesson lookup table.

    Returns
    -------

    {
        "intro": Path(...),
        "di": Path(...),
    }
    """

    return {file.stem: file for file in scan_lessons(lessons_dir)}
