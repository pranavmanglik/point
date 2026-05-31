"""
point.builders.glossary
~~~~~~~~~~~~~~~~~~~~~~~

Glossary generation system.

Responsibilities
----------------

Generate glossary resources from
Point educational content.

Features
--------

- glossary extraction
- glossary markdown generation
- glossary json generation

Pipeline
--------

Lessons
    ↓

Parser
    ↓

AST
    ↓

GlossaryBuilder
    ↓

glossary.json
glossary/index.md

Overview
--------

GlossaryBuilder scans lesson ASTs and extracts all
Term nodes.

Example
-------

Point:

    @term Dependency Injection

    Providing dependencies externally.

    @end

Generated JSON:

    {
        "term": "Dependency Injection",
        "definition": "Providing dependencies externally.",
        "lesson": "dependency-injection"
    }

Generated Markdown:

    ## Dependency Injection

    Providing dependencies externally.
"""

from __future__ import annotations

import json
from dataclasses import (
    dataclass,
)
from pathlib import (
    Path,
)

from point.ast.nodes import (
    Definition,
    Lesson,
    Term,
)


@dataclass(slots=True)
class GlossaryEntry:
    """
    Represents a single glossary entry.

    Attributes
    ----------

    term:
        Glossary term name.

    definition:
        Term definition.

    lesson:
        Source lesson title.
    """

    term: str

    definition: str

    lesson: str


class GlossaryBuilder:
    """
    Build glossary resources.

    Output
    ------

    glossary.json

    glossary/index.md
    """

    def build(
        self,
        lessons: list[Lesson],
        output_dir: Path,
    ) -> None:
        """
        Build glossary resources.

        Parameters
        ----------

        lessons:
            Parsed lesson ASTs.

        output_dir:
            Glossary output directory.
        """

        entries = self.extract_entries(lessons)

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.write_json(
            entries,
            output_dir / "glossary.json",
        )

        self.write_markdown(
            entries,
            output_dir / "index.md",
        )

    def extract_entries(
        self,
        lessons: list[Lesson],
    ) -> list[GlossaryEntry]:
        """
        Extract glossary entries from lessons.

        Parameters
        ----------

        lessons:
            Parsed lesson ASTs.

        Returns
        -------

        list[GlossaryEntry]
        """

        entries: list[GlossaryEntry] = []

        for lesson in lessons:
            for node in lesson.children:
                if not isinstance(
                    node,
                    (Term, Definition),
                ):
                    continue

                entries.append(
                    GlossaryEntry(
                        term=node.title,
                        definition=node.content,
                        lesson=lesson.title,
                    )
                )

        entries.sort(key=lambda entry: entry.term.lower())

        return entries

    def write_json(
        self,
        entries: list[GlossaryEntry],
        output_file: Path,
    ) -> None:
        """
        Write glossary JSON.

        Parameters
        ----------

        entries:
            Glossary entries.

        output_file:
            JSON output path.
        """

        data = [
            {
                "term": entry.term,
                "definition": entry.definition,
                "lesson": entry.lesson,
            }
            for entry in entries
        ]

        output_file.write_text(
            json.dumps(
                data,
                indent=4,
            ),
            encoding="utf-8",
        )

    def write_markdown(
        self,
        entries: list[GlossaryEntry],
        output_file: Path,
    ) -> None:
        """
        Write glossary markdown page.

        Parameters
        ----------

        entries:
            Glossary entries.

        output_file:
            Markdown output path.
        """

        lines = [
            "# Glossary",
            "",
        ]

        if not entries:
            lines.extend(
                [
                    "No glossary entries found.",
                    "",
                    "Add terms using:",
                    "",
                    "```txt",
                    "@term Example",
                    "",
                    "Description of the term.",
                    "",
                    "@end",
                    "```",
                    "",
                ]
            )

        for entry in entries:
            lines.extend(
                [
                    f"## {entry.term}",
                    "",
                    entry.definition,
                    "",
                    f"> Source: {entry.lesson}",
                    "",
                ]
            )

        output_file.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )
