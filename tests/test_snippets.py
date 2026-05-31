"""
tests.test_snippets
~~~~~~~~~~~~~~~~~~~

Tests for reusable snippet generation.

Responsibilities
----------------

Verify snippet extraction and
resource generation.

Coverage
--------

- snippet extraction
- duplicate validation
- registry generation
- json generation
- full build pipeline
"""

from pathlib import Path

import pytest

from point.ast.nodes import (
    Lesson,
    Snippet,
)
from point.builders.snippets import (
    SnippetBuilder,
)


def test_extract_snippets():
    """
    Extract snippets from lessons.
    """

    lesson = Lesson(
        title="Dependency Injection",
    )

    lesson.children.append(
        Snippet(
            name="container",
            content="Container example.",
        )
    )

    snippets = SnippetBuilder().extract_snippets([lesson])

    assert len(snippets) == 1

    snippet = snippets[0]

    assert snippet.name == "container"

    assert snippet.content == "Container example."

    assert snippet.lesson == "Dependency Injection"


def test_extract_snippets_sorted():
    """
    Snippets should be sorted
    alphabetically.
    """

    lesson = Lesson(
        title="Test",
    )

    lesson.children.extend(
        [
            Snippet(
                name="zeta",
                content="z",
            ),
            Snippet(
                name="alpha",
                content="a",
            ),
        ]
    )

    snippets = SnippetBuilder().extract_snippets([lesson])

    assert snippets[0].name == "alpha"

    assert snippets[1].name == "zeta"


def test_duplicate_snippets_raise():
    """
    Duplicate snippets should
    raise an error.
    """

    lesson = Lesson(
        title="Test",
    )

    lesson.children.extend(
        [
            Snippet(
                name="container",
                content="A",
            ),
            Snippet(
                name="container",
                content="B",
            ),
        ]
    )

    with pytest.raises(
        ValueError,
    ):
        (SnippetBuilder().extract_snippets([lesson]))


def test_build_registry():
    """
    Build snippet lookup registry.
    """

    lesson = Lesson(
        title="Test",
    )

    lesson.children.append(
        Snippet(
            name="container",
            content="Example",
        )
    )

    registry = SnippetBuilder().build_registry([lesson])

    assert registry["container"] == "Example"


def test_write_json(
    tmp_path: Path,
):
    """
    Generate snippets JSON.
    """

    lesson = Lesson(
        title="Test",
    )

    lesson.children.append(
        Snippet(
            name="container",
            content="Example",
        )
    )

    builder = SnippetBuilder()

    snippets = builder.extract_snippets([lesson])

    output_file = tmp_path / "snippets.json"

    builder.write_json(
        snippets,
        output_file,
    )

    assert output_file.exists()

    content = output_file.read_text(
        encoding="utf-8",
    )

    assert "container" in content


def test_build(
    tmp_path: Path,
):
    """
    Build complete snippet resources.
    """

    lesson = Lesson(
        title="Test",
    )

    lesson.children.append(
        Snippet(
            name="container",
            content="Example",
        )
    )

    SnippetBuilder().build(
        [lesson],
        tmp_path,
    )

    assert (tmp_path / "snippets.json").exists()
