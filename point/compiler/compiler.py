"""
point.compiler.compiler
~~~~~~~~~~~~~~~~~~~~~~~

Markdown compiler for Point.

The compiler transforms Point AST nodes into
VitePress-compatible markdown.

Pipeline
--------

Point Source
      ↓
Tokenizer
      ↓
Parser
      ↓
AST
      ↓
Compiler
      ↓
Markdown

The compiler is intentionally stateless.

Future compiler outputs may include:

- glossary.json
- graph.json
- paths.json
- component metadata
"""

from point.ast.nodes import (
    BestPractice,
    Code,
    Component,
    Concept,
    Concepts,
    Danger,
    Definition,
    Diagram,
    Equation,
    Figure,
    Gallery,
    Goals,
    Image,
    Include,
    Info,
    Interview,
    Lesson,
    Math,
    Meta,
    Note,
    Path,
    Pitfall,
    Reading,
    References,
    Related,
    Section,
    Snippet,
    Summary,
    Term,
    Theorem,
    Tip,
    Use,
    Version,
    Warning,
)


class MarkdownCompiler:
    """
    Compile Point AST into markdown.
    """

    def __init__(
        self,
        snippets: dict[str, str] | None = None,
    ):
        self.snippets = snippets or {}

    def compile(
        self,
        lesson: Lesson,
    ) -> str:

        output: list[str] = []

        #
        # Frontmatter
        #

        meta = self._find_meta(lesson)

        if meta:
            output.extend(
                self._compile_frontmatter(
                    lesson,
                    meta,
                )
            )

        else:
            output.extend(
                [
                    "---",
                    f'title: "{lesson.title}"',
                    "---",
                ]
            )

        output.append(f"# {lesson.title}")

        #
        # Body
        #

        for node in lesson.children:
            if isinstance(
                node,
                Meta,
            ):
                continue

            output.extend(self._compile_node(node))

        return "\n".join(output)

    def _find_meta(
        self,
        lesson: Lesson,
    ):

        for node in lesson.children:
            if isinstance(
                node,
                Meta,
            ):
                return node

        return None

    def _compile_frontmatter(
        self,
        lesson: Lesson,
        meta: Meta,
    ) -> list[str]:

        lines = [
            "---",
            f'title: "{lesson.title}"',
        ]

        for key, value in meta.values.items():
            lines.append(f"{key}: {value}")

        lines.append("---")

        return lines

    def _compile_node(
        self,
        node,
    ) -> list[str]:

        #
        # Goals
        #

        if isinstance(
            node,
            Goals,
        ):
            lines = ["## Goals"]

            lines.extend(f"- {item}" for item in node.items)

            return lines

        #
        # Summary
        #

        if isinstance(
            node,
            Summary,
        ):
            return [
                "## Summary",
                node.content,
            ]

        #
        # Sections
        #

        if isinstance(
            node,
            Section,
        ):
            return [
                f"## {node.title}",
                node.content,
            ]

        #
        # Educational Blocks
        #

        if isinstance(
            node,
            Definition,
        ):
            return [
                f"## Definition: {node.title}",
                node.content,
            ]

        if isinstance(
            node,
            Term,
        ):
            return [
                f"## Term: {node.title}",
                node.content,
            ]

        if isinstance(
            node,
            Concept,
        ):
            return [
                f"## Concept: {node.title}",
                node.content,
            ]

        #
        # Content Blocks
        #

        admonitions = {
            Note: "info",
            Tip: "tip",
            Warning: "warning",
            Danger: "danger",
            Info: "info",
        }

        for cls, kind in admonitions.items():
            if isinstance(
                node,
                cls,
            ):
                return [
                    f"::: {kind}",
                    node.content,
                    ":::",
                ]

        #
        # Practice Blocks
        #

        if isinstance(
            node,
            Pitfall,
        ):
            return [
                "::: warning",
                node.content,
                ":::",
            ]

        if isinstance(
            node,
            BestPractice,
        ):
            return [
                "::: tip",
                node.content,
                ":::",
            ]

        if isinstance(
            node,
            Interview,
        ):
            return [
                "### Interview Question",
                node.content,
            ]

        #
        # Code
        #

        if isinstance(
            node,
            Code,
        ):
            return [
                f"```{node.language}",
                node.content,
                "```",
            ]

        #
        # Diagram
        #

        if isinstance(
            node,
            Diagram,
        ):
            if isinstance(node, Diagram):
                if node.diagram_type == "mermaid":
                    content = (
                        node.content
                        .replace("\\", "\\\\")
                        .replace('"', '\\"')
                    )
            
                    return [
                        f'<MermaidDiagram :chart="`{node.content}`" />',
                        "",
                    ]
        
            return [
                f"```{node.diagram_type}",
                node.content,
                "```",
            ]
            
        #
        # Image
        #

        if isinstance(
            node,
            Image,
        ):
            return [f"![{node.caption or ''}]({node.path})"]

        #
        # Figure
        #

        if isinstance(
            node,
            Figure,
        ):
            return [
                "<figure>",
                f'<img src="{node.path}" />',
                f"<figcaption>{node.caption or ''}</figcaption>",
                "</figure>",
            ]

        #
        # Gallery
        #

        if isinstance(
            node,
            Gallery,
        ):
            lines = ["## Gallery"]

            lines.extend(f"![]({image})" for image in node.images)

            return lines

        #
        # Mathematics
        #

        if isinstance(
            node,
            (
                Math,
                Equation,
            ),
        ):
            return [
                "$$",
                node.content,
                "$$",
            ]

        if isinstance(
            node,
            Theorem,
        ):
            return [
                f"## Theorem: {node.title}",
                node.content,
            ]

        #
        # References
        #

        if isinstance(
            node,
            References,
        ):
            lines = ["## References"]

            lines.extend(f"- {item}" for item in node.items)

            return lines

        if isinstance(
            node,
            Reading,
        ):
            lines = ["## Further Reading"]

            lines.extend(f"- {item}" for item in node.items)

            return lines

        #
        # Related Topics
        #

        if isinstance(
            node,
            Related,
        ):
            lines = ["## Related Topics"]

            lines.extend(f"- {item}" for item in node.lessons)

            return lines

        #
        # Concepts
        #

        if isinstance(
            node,
            Concepts,
        ):
            lines = ["## Concepts"]

            lines.extend(f"- {item}" for item in node.items)

            return lines

        #
        # Include
        #

        if isinstance(
            node,
            Include,
        ):
            return [f"<!-- include:{node.path} -->"]

        #
        # Snippets
        #

        if isinstance(
            node,
            Snippet,
        ):
            #
            # Snippets are registry content.
            #
            # They should not render directly.
            #

            return []

        #
        # Snippet Usage
        #

        if isinstance(
            node,
            Use,
        ):
            content = self.snippets.get(node.name)

            if content is None:
                return [f"<!-- missing snippet: {node.name} -->"]

            return [content]

        #
        # Learning Paths
        #

        if isinstance(
            node,
            Path,
        ):
            lines = [f"## Path: {node.title}"]

            lines.extend(
                f"{i + 1}. {item}" for i, item in enumerate(node.lessons)
            )

            return lines

        #
        # Version
        #

        if isinstance(
            node,
            Version,
        ):
            lines = [f"## Version {node.version}"]

            for child in node.children:
                lines.extend(self._compile_node(child))

            return lines

        #
        # Components
        #

        if isinstance(
            node,
            Component,
        ):
            return [f"<{node.name} />"]

        return []
