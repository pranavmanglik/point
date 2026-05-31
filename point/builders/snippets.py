"""
point.builders.snippets
~~~~~~~~~~~~~~~~~~~~~~~

Reusable content generation system.

Responsibilities
----------------

Extract reusable content snippets
from Point lessons.

Features
--------

- snippet extraction
- snippet registry generation
- snippet validation
- json generation

Pipeline
--------

Lessons
    ↓

Parser
    ↓

AST
    ↓

SnippetBuilder
    ↓

snippets.json

Overview
--------

Snippets provide reusable educational
content across lessons.

Example
-------

@snippet dependency-injection

Dependencies should be supplied
from the outside.

@end

Produces:

{
    "name": "dependency-injection",
    "content": "...",
    "lesson": "Dependency Injection"
}
"""

from __future__ import annotations

import json
from dataclasses import (
    asdict,
    dataclass,
)
from pathlib import (
    Path,
)

from point.ast.nodes import (
    Lesson,
    Snippet,
)


@dataclass(slots=True)
class SnippetEntry:
    """
    Registered snippet.

    Attributes
    ----------

    name:
        Unique snippet identifier.

    content:
        Reusable content.

    lesson:
        Source lesson.
    """

    name: str

    content: str

    lesson: str


class SnippetBuilder:
    """
    Build reusable snippet resources.

    Outputs
    -------

    snippets.json
    """

    def build(
        self,
        lessons: list[Lesson],
        output_dir: Path,
    ) -> None:
        """
        Build snippet resources.

        Parameters
        ----------
        lessons:
            Parsed lesson ASTs.

        output_dir:
            Output directory.
        """

        snippets = self.extract_snippets(lessons)

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.write_json(
            snippets,
            output_dir / "snippets.json",
        )

    def extract_snippets(
        self,
        lessons: list[Lesson],
    ) -> list[SnippetEntry]:
        """
        Extract snippets from lessons.

        Parameters
        ----------
        lessons:
            Parsed lesson ASTs.

        Returns
        -------
        list[SnippetEntry]
        """

        snippets: list[SnippetEntry] = []

        seen: set[str] = set()

        for lesson in lessons:
            for node in lesson.children:
                if not isinstance(
                    node,
                    Snippet,
                ):
                    continue

                if node.name in seen:
                    raise ValueError(f"Duplicate snippet: {node.name}")

                seen.add(node.name)

                snippets.append(
                    SnippetEntry(
                        name=node.name,
                        content=node.content,
                        lesson=lesson.title,
                    )
                )

        snippets.sort(key=lambda snippet: snippet.name.lower())

        return snippets

    def build_registry(
        self,
        lessons: list[Lesson],
    ) -> dict[str, str]:
        """
        Build snippet lookup registry.
        """

        registry = {}

        for snippet in self.extract_snippets(lessons):
            registry[snippet.name] = snippet.content

        return registry

    def write_json(
        self,
        snippets: list[SnippetEntry],
        output_file: Path,
    ) -> None:
        """
        Write snippet registry.

        Parameters
        ----------
        snippets:
            Registered snippets.

        output_file:
            Output JSON file.
        """

        data = [asdict(snippet) for snippet in snippets]

        output_file.write_text(
            json.dumps(
                data,
                indent=4,
            ),
            encoding="utf-8",
        )
