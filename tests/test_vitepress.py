"""
tests.test_vitepress
~~~~~~~~~~~~~~~~~~~~

Tests for VitePress generation.

Responsibilities
----------------

Verify VitePress resource generation.

Coverage
--------

- index generation
- sidebar generation
- theme generation
- config generation
"""

from pathlib import Path

from point.vitepress.generator import (
    generate_config,
    generate_index,
    generate_sidebar,
    generate_theme,
)


def test_generate_index(
    tmp_path: Path,
):
    """
    Generate default home page.
    """

    generate_index(tmp_path)

    index_file = tmp_path / "index.md"

    assert index_file.exists()

    content = index_file.read_text(
        encoding="utf-8",
    )

    assert "# Welcome" in content

    assert "Glossary" in content

    assert "Knowledge Graph" in content


def test_generate_sidebar():
    """
    Generate lesson sidebar.
    """

    docs_dir = Path("tests-temp-sidebar")

    docs_dir.mkdir(
        exist_ok=True,
    )

    try:
        (docs_dir / "intro.md").write_text(
            "",
            encoding="utf-8",
        )

        (docs_dir / "advanced-topics.md").write_text(
            "",
            encoding="utf-8",
        )

        sidebar = generate_sidebar(docs_dir)

        assert "Intro" in sidebar

        assert "Advanced Topics" in sidebar

    finally:
        for file in docs_dir.glob("*"):
            file.unlink()

        docs_dir.rmdir()


def test_generate_theme(
    tmp_path: Path,
):
    """
    Generate VitePress theme.
    """

    generate_theme(tmp_path)

    theme_dir = tmp_path / ".vitepress" / "theme"

    assert theme_dir.exists()

    assert (theme_dir / "custom.css").exists()

    assert (theme_dir / "index.ts").exists()


def test_generate_config(
    tmp_path: Path,
):
    """
    Generate VitePress config.
    """

    (tmp_path / "lesson.md").write_text(
        "# Lesson",
        encoding="utf-8",
    )

    generate_config(
        title="Point Course",
        docs_dir=tmp_path,
    )

    config_file = tmp_path / ".vitepress" / "config.mts"

    assert config_file.exists()

    content = config_file.read_text(
        encoding="utf-8",
    )

    assert "Point Course" in content

    assert "Glossary" in content


def test_generate_config_github_pages(
    tmp_path: Path,
):
    """
    Generate GitHub Pages config.
    """

    generate_config(
        title="Point",
        docs_dir=tmp_path,
        base="/point/",
    )

    config_file = tmp_path / ".vitepress" / "config.mts"

    content = config_file.read_text(
        encoding="utf-8",
    )

    assert 'base: "/point/"' in content
