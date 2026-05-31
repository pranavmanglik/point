"""
tests.test_scanner
~~~~~~~~~~~~~~~~~~

Tests for project scanning.

Responsibilities
----------------

Verify project discovery utilities.

Coverage
--------

- lesson scanning
- generic directory scanning
- lesson names
- lesson lookup maps
"""

from pathlib import Path

from point.project.scanner import (
    lesson_map,
    lesson_names,
    scan_directory,
    scan_lessons,
)


def test_scan_lessons(
    tmp_path: Path,
):
    """
    Discover Point lessons.
    """

    (tmp_path / "intro.point").write_text("")

    (tmp_path / "advanced.point").write_text("")

    lessons = scan_lessons(tmp_path)

    assert len(lessons) == 2

    assert lessons[0].name == "advanced.point"

    assert lessons[1].name == "intro.point"


def test_scan_directory(
    tmp_path: Path,
):
    """
    Scan arbitrary extension.
    """

    (tmp_path / "a.md").write_text("")

    (tmp_path / "b.md").write_text("")

    files = scan_directory(
        tmp_path,
        "md",
    )

    assert len(files) == 2


def test_lesson_names(
    tmp_path: Path,
):
    """
    Return lesson stems.
    """

    (tmp_path / "intro.point").write_text("")

    (tmp_path / "advanced.point").write_text("")

    names = lesson_names(tmp_path)

    assert "intro" in names

    assert "advanced" in names


def test_lesson_map(
    tmp_path: Path,
):
    """
    Create lesson lookup table.
    """

    intro = tmp_path / "intro.point"

    intro.write_text("")

    mapping = lesson_map(tmp_path)

    assert "intro" in mapping

    assert mapping["intro"] == intro
