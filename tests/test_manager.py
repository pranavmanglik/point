"""
tests.test_manager
~~~~~~~~~~~~~~~~~~

Tests for project management.

Responsibilities
----------------

Verify project path resolution and
directory management.

Coverage
--------

- project initialization
- path resolution
- lesson paths
- markdown paths
- glossary paths
- graph paths
- learning path paths
"""

from pathlib import Path

from point.project.creator import (
    create_project,
)
from point.project.manager import (
    ProjectManager,
)


def test_project_manager_init(
    tmp_path: Path,
    monkeypatch,
):
    """
    Initialize project manager.
    """

    create_project(tmp_path)

    monkeypatch.chdir(tmp_path)

    project = ProjectManager()

    assert project.root == tmp_path

    assert project.lessons_dir == tmp_path / "lessons"

    assert project.docs_dir == tmp_path / "docs"


def test_resolve(
    tmp_path: Path,
    monkeypatch,
):
    """
    Resolve project-relative paths.
    """

    create_project(tmp_path)

    monkeypatch.chdir(tmp_path)

    project = ProjectManager()

    resolved = project.resolve(
        "docs",
        "intro.md",
    )

    assert resolved == tmp_path / "docs" / "intro.md"


def test_lesson_path(
    tmp_path: Path,
    monkeypatch,
):
    """
    Resolve lesson file.
    """

    create_project(tmp_path)

    monkeypatch.chdir(tmp_path)

    project = ProjectManager()

    assert project.lesson_path("intro") == tmp_path / "lessons" / "intro.point"


def test_markdown_path(
    tmp_path: Path,
    monkeypatch,
):
    """
    Resolve markdown file.
    """

    create_project(tmp_path)

    monkeypatch.chdir(tmp_path)

    project = ProjectManager()

    assert project.markdown_path("intro") == tmp_path / "docs" / "intro.md"


def test_glossary_path(
    tmp_path: Path,
    monkeypatch,
):
    """
    Resolve glossary page.
    """

    create_project(tmp_path)

    monkeypatch.chdir(tmp_path)

    project = ProjectManager()

    assert project.glossary_path() == tmp_path / "glossary" / "index.md"


def test_graph_path(
    tmp_path: Path,
    monkeypatch,
):
    """
    Resolve graph resource.
    """

    create_project(tmp_path)

    monkeypatch.chdir(tmp_path)

    project = ProjectManager()

    assert project.graph_path() == tmp_path / "graph" / "graph.json"


def test_paths_path(
    tmp_path: Path,
    monkeypatch,
):
    """
    Resolve learning paths page.
    """

    create_project(tmp_path)

    monkeypatch.chdir(tmp_path)

    project = ProjectManager()

    assert project.paths_path() == tmp_path / "paths" / "index.md"
