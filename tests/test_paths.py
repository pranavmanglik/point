"""
tests.test_paths
~~~~~~~~~~~~~~~~

Tests for learning path generation.

Responsibilities
----------------

Verify learning path extraction and
resource generation.

Coverage
--------

- path extraction
- duplicate removal
- alphabetical sorting
- json generation
- markdown generation
- full build pipeline
"""

from pathlib import Path

from point.ast.nodes import (
    Lesson,
)
from point.ast.nodes import (
    Path as PathNode,
)
from point.builders.paths import (
    PathBuilder,
)


def test_extract_paths():
    """
    Extract learning paths from lessons.
    """

    lesson = Lesson(
        title="Dependency Injection",
    )

    lesson.children.append(
        PathNode(
            title="Backend",
            lessons=[
                "HTTP",
                "REST",
                "Authentication",
            ],
        )
    )

    paths = PathBuilder().extract_paths([lesson])

    assert len(paths) == 1

    path = paths[0]

    assert path.title == "Backend"

    assert path.lessons == [
        "HTTP",
        "REST",
        "Authentication",
    ]


def test_extract_paths_sorted():
    """
    Learning paths should be sorted
    alphabetically.
    """

    lesson = Lesson(
        title="Test",
    )

    lesson.children.extend(
        [
            PathNode(
                title="Zoo",
                lessons=["A"],
            ),
            PathNode(
                title="Alpha",
                lessons=["B"],
            ),
        ]
    )

    paths = PathBuilder().extract_paths([lesson])

    assert paths[0].title == "Alpha"

    assert paths[1].title == "Zoo"


def test_duplicate_paths_removed():
    """
    Duplicate paths should be ignored.
    """

    lesson = Lesson(
        title="Test",
    )

    lesson.children.extend(
        [
            PathNode(
                title="Backend",
                lessons=["HTTP"],
            ),
            PathNode(
                title="Backend",
                lessons=["REST"],
            ),
        ]
    )

    paths = PathBuilder().extract_paths([lesson])

    assert len(paths) == 1


def test_write_json(
    tmp_path: Path,
):
    """
    Generate paths JSON.
    """

    lesson = Lesson(
        title="Test",
    )

    lesson.children.append(
        PathNode(
            title="Backend",
            lessons=[
                "HTTP",
                "REST",
            ],
        )
    )

    builder = PathBuilder()

    paths = builder.extract_paths([lesson])

    output_file = tmp_path / "paths.json"

    builder.write_json(
        paths,
        output_file,
    )

    assert output_file.exists()

    content = output_file.read_text(
        encoding="utf-8",
    )

    assert "Backend" in content

    assert "HTTP" in content


def test_write_markdown(
    tmp_path: Path,
):
    """
    Generate learning paths page.
    """

    lesson = Lesson(
        title="Test",
    )

    lesson.children.append(
        PathNode(
            title="Backend",
            lessons=[
                "HTTP",
                "REST",
            ],
        )
    )

    builder = PathBuilder()

    paths = builder.extract_paths([lesson])

    output_file = tmp_path / "index.md"

    builder.write_markdown(
        paths,
        output_file,
    )

    assert output_file.exists()

    content = output_file.read_text(
        encoding="utf-8",
    )

    assert "Learning Paths" in content

    assert "Backend" in content


def test_build(
    tmp_path: Path,
):
    """
    Build complete path resources.
    """

    lesson = Lesson(
        title="Test",
    )

    lesson.children.append(
        PathNode(
            title="Backend",
            lessons=[
                "HTTP",
                "REST",
            ],
        )
    )

    PathBuilder().build(
        [lesson],
        tmp_path,
    )

    assert (tmp_path / "paths.json").exists()

    assert (tmp_path / "index.md").exists()
