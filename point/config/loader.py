"""
point.config.loader
~~~~~~~~~~~~~~~~~~~

Configuration loading utilities.

This module is responsible for locating and loading
Point project configuration files.

Pipeline
--------

point.toml
      ↓
find_config()
      ↓
tomllib
      ↓
ProjectConfig
      ↓
Application

Responsibilities
----------------

- locate point.toml
- parse TOML configuration
- populate config models
- apply defaults
"""

import tomllib
from pathlib import Path

from point.config.model import (
    BuildConfig,
    ProjectConfig,
    ThemeConfig,
)


def find_config() -> Path:
    """
    Locate point.toml.

    Searches upward from the current working
    directory until a Point project is found.
    """

    current = Path.cwd()

    while current != current.parent:
        config = current / "point.toml"

        if config.exists():
            return config

        current = current.parent

    raise FileNotFoundError("point.toml not found")


def load_config() -> ProjectConfig:
    """
    Load Point configuration.

    Returns
    -------
    ProjectConfig
    """

    config_path = find_config()

    with open(
        config_path,
        "rb",
    ) as file:
        data = tomllib.load(file)

    #
    # Theme
    #

    theme_data = data.get(
        "theme",
        {},
    )

    theme = ThemeConfig(
        logo=theme_data.get(
            "logo",
            "",
        ),
        favicon=theme_data.get(
            "favicon",
            "",
        ),
        accent_color=theme_data.get(
            "accent_color",
            "#646cff",
        ),
        dark_mode=theme_data.get(
            "dark_mode",
            True,
        ),
    )

    #
    # Build
    #

    build_data = data.get(
        "build",
        {},
    )

    build = BuildConfig(
        glossary=build_data.get(
            "glossary",
            True,
        ),
        knowledge_graph=build_data.get(
            "knowledge_graph",
            True,
        ),
        learning_paths=build_data.get(
            "learning_paths",
            True,
        ),
        components=build_data.get(
            "components",
            True,
        ),
        versioning=build_data.get(
            "versioning",
            True,
        ),
    )

    #
    # Project
    #

    return ProjectConfig(
        title=data.get(
            "title",
            "Point Project",
        ),
        author=data.get(
            "author",
            "",
        ),
        github_pages=data.get(
            "github_pages",
            False,
        ),
        version=data.get(
            "version",
            "1.0.0",
        ),
        description=data.get(
            "description",
            "",
        ),
        learning_path=data.get(
            "learning_path",
        ),
        lessons_dir=data.get(
            "lessons_dir",
            "lessons",
        ),
        docs_dir=data.get(
            "docs_dir",
            "docs",
        ),
        assets_dir=data.get(
            "assets_dir",
            "assets",
        ),
        components_dir=data.get(
            "components_dir",
            "components",
        ),
        glossary_dir=data.get(
            "glossary_dir",
            "glossary",
        ),
        graph_dir=data.get(
            "graph_dir",
            "graph",
        ),
        paths_dir=data.get(
            "paths_dir",
            "paths",
        ),
        theme=theme,
        build=build,
    )
