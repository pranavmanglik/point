"""
point.builders.graph
~~~~~~~~~~~~~~~~~~~~

Knowledge graph generation system.

Responsibilities
----------------

Generate educational knowledge graphs
from Point lessons.

Features
--------

- node extraction
- edge extraction
- graph json generation

Pipeline
--------

Lessons
    ↓

Parser
    ↓

AST
    ↓

GraphBuilder
    ↓

graph.json

Overview
--------

The knowledge graph provides the foundation for:

- concept exploration
- glossary linking
- lesson recommendations
- learning paths
- prerequisite analysis

Graph generation is intentionally independent
from visualization systems.

The output is pure JSON that may later be
consumed by VitePress components or external
graph visualization tools.
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
    Concept,
    Definition,
    Lesson,
    Related,
    Term,
    Theorem,
)


@dataclass(slots=True)
class GraphNode:
    """
    Knowledge graph node.

    Attributes
    ----------

    id:
        Unique identifier.

    label:
        Human-readable name.

    type:
        Node category.
    """

    id: str

    label: str

    type: str

    content: str = ""


@dataclass(slots=True)
class GraphEdge:
    """
    Knowledge graph edge.

    Attributes
    ----------

    source:
        Source node id.

    target:
        Target node id.

    relation:
        Relationship type.
    """

    source: str

    target: str

    relation: str


class GraphBuilder:
    """
    Build educational knowledge graphs.
    """

    def build(
        self,
        lessons: list[Lesson],
        output_dir: Path,
    ) -> None:
        """
        Build graph resources.

        Parameters
        ----------

        lessons:
            Parsed lesson ASTs.

        output_dir:
            Graph output directory.
        """

        nodes = self.extract_nodes(lessons)

        edges = self.extract_edges(lessons)

        valid_nodes = {node.id for node in nodes}

        edges = [
            edge
            for edge in edges
            if edge.source in valid_nodes and edge.target in valid_nodes
        ]

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.write_json(
            nodes,
            edges,
            output_dir / "graph.json",
        )

        self.write_markdown(
            nodes,
            edges,
            output_dir / "index.md",
        )

    def extract_nodes(
        self,
        lessons: list[Lesson],
    ) -> list[GraphNode]:
        """
        Extract graph nodes from lessons.
        """

        nodes: list[GraphNode] = []

        seen: set[str] = set()

        for lesson in lessons:
            lesson_id = self.slugify(lesson.title)

            if lesson_id not in seen:
                seen.add(lesson_id)

                nodes.append(
                    GraphNode(
                        id=lesson_id,
                        label=lesson.title,
                        type="lesson",
                        content="",
                    )
                )

            for node in lesson.children:
                if isinstance(
                    node,
                    Term,
                ):
                    graph_node = GraphNode(
                        id=self.slugify(node.title),
                        label=node.title,
                        type="term",
                        content=node.content,
                    )

                elif isinstance(
                    node,
                    Definition,
                ):
                    graph_node = GraphNode(
                        id=self.slugify(node.title),
                        label=node.title,
                        type="definition",
                    )

                elif isinstance(
                    node,
                    Concept,
                ):
                    graph_node = GraphNode(
                        id=self.slugify(node.title),
                        label=node.title,
                        type="concept",
                    )

                elif isinstance(
                    node,
                    Theorem,
                ):
                    graph_node = GraphNode(
                        id=self.slugify(node.title),
                        label=node.title,
                        type="theorem",
                    )

                else:
                    continue

                if graph_node.id in seen:
                    continue

                seen.add(graph_node.id)

                nodes.append(graph_node)

        return nodes

    def extract_edges(
        self,
        lessons: list[Lesson],
    ) -> list[GraphEdge]:
        """
        Extract graph edges.
        """

        edges: list[GraphEdge] = []

        for lesson in lessons:
            lesson_id = self.slugify(lesson.title)

            for node in lesson.children:
                #
                # Lesson contains concept
                #

                if isinstance(
                    node,
                    (
                        Term,
                        Definition,
                        Concept,
                        Theorem,
                    ),
                ):
                    edges.append(
                        GraphEdge(
                            source=lesson_id,
                            target=self.slugify(node.title),
                            relation="contains",
                        )
                    )

                #
                # Explicit related links
                #

                if not isinstance(
                    node,
                    Related,
                ):
                    continue

                for item in node.lessons:
                    edges.append(
                        GraphEdge(
                            source=lesson_id,
                            target=self.slugify(item),
                            relation="related",
                        )
                    )

        return edges

    def write_json(
        self,
        nodes: list[GraphNode],
        edges: list[GraphEdge],
        output_file: Path,
    ) -> None:
        """
        Write graph JSON.
        """

        data = {
            "nodes": [asdict(node) for node in nodes],
            "edges": [asdict(edge) for edge in edges],
        }

        output_file.write_text(
            json.dumps(
                data,
                indent=4,
            ),
            encoding="utf-8",
        )

    def write_markdown(
        self,
        nodes: list[GraphNode],
        edges: list[GraphEdge],
        output_file: Path,
    ) -> None:
        output_file.write_text(
            "\n".join(
                [
                    "# Knowledge Graph",
                    "",
                    "<GraphViewer />",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    def slugify(
        self,
        value: str,
    ) -> str:
        """
        Convert text into a graph id.
        """

        return value.strip().lower().replace(" ", "-")
