"""
point.parser.parser
~~~~~~~~~~~~~~~~~~~

Parser implementation for Point.

The parser converts lexical tokens into an
Abstract Syntax Tree (AST).

Point 1.0 Parsing Model
-----------------------

Every block directive follows:

    @directive [optional argument]

    content

    @end

Examples:

    @warning

    Avoid service locators.

    @end

    @section Introduction

    Dependency injection reduces coupling.

    @end

The parser is responsible for:

- directive interpretation
- block collection
- AST node creation
- lesson construction
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
    Next,
    Note,
    Path,
    Pitfall,
    Previous,
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
from point.errors import (
    MissingEndDirectiveError,
)
from point.tokenizer.token import (
    Token,
    TokenType,
)


class Parser:
    """
    Point parser.
    """

    def parse(
        self,
        tokens: list[Token],
    ) -> Lesson:

        lesson: Lesson | None = None

        i = 0

        while i < len(tokens):
            token = tokens[i]

            if token.type != TokenType.DIRECTIVE:
                i += 1
                continue

            #
            # Lesson
            #

            if token.value == "lesson":
                title = self._text_after(
                    tokens,
                    i,
                )

                lesson = Lesson(
                    title=title,
                )

                i += 2
                continue

            if lesson is None:
                raise ValueError("Lesson must be declared first.")

            #
            # Meta
            #

            if token.value == "meta":
                block, i = self._collect_block(
                    tokens,
                    i + 1,
                    "meta",
                )

                values = {}

                for line in block:
                    if ":" not in line:
                        continue

                    key, value = line.split(
                        ":",
                        maxsplit=1,
                    )

                    values[key.strip()] = value.strip()

                lesson.children.append(
                    Meta(
                        values=values,
                    )
                )

                continue

            #
            # Goals
            #

            if token.value == "goals":
                block, i = self._collect_block(
                    tokens,
                    i + 1,
                    "goals",
                )

                lesson.children.append(
                    Goals(items=[item.lstrip("- ").strip() for item in block])
                )

                continue

            #
            # Generic content blocks
            #

            block_nodes = {
                "note": Note,
                "tip": Tip,
                "warning": Warning,
                "danger": Danger,
                "info": Info,
                "pitfall": Pitfall,
                "bestpractice": BestPractice,
                "interview": Interview,
                "math": Math,
                "equation": Equation,
                "summary": Summary,
            }

            if token.value in block_nodes:
                block, i = self._collect_block(
                    tokens,
                    i + 1,
                    token.value,
                )

                lesson.children.append(
                    block_nodes[token.value](content="\n".join(block))
                )

                continue

            #
            # Titled blocks
            #

            titled_nodes = {
                "section": Section,
                "definition": Definition,
                "term": Term,
                "concept": Concept,
                "theorem": Theorem,
            }

            if token.value in titled_nodes:
                title = self._text_after(
                    tokens,
                    i,
                )

                block, i = self._collect_block(
                    tokens,
                    i + 2,
                    token.value,
                )

                lesson.children.append(
                    titled_nodes[token.value](
                        title=title,
                        content="\n".join(block),
                    )
                )

                continue

            #
            # Path
            #

            if token.value == "path":
                title = self._text_after(
                    tokens,
                    i,
                )

                block, i = self._collect_block(
                    tokens,
                    i + 2,
                    "path",
                )

                lesson.children.append(
                    Path(
                        title=title,
                        lessons=block,
                    )
                )

                continue

            #
            # Version
            #

            if token.value == "version":
                version = self._text_after(
                    tokens,
                    i,
                )

                lesson.children.append(
                    Version(
                        version=version,
                        children=[],
                    )
                )

                i += 2
                continue

            #
            # Code
            #

            if token.value == "code":
                language = self._text_after(
                    tokens,
                    i,
                )

                block, i = self._collect_block(
                    tokens,
                    i + 2,
                    "code",
                )

                lesson.children.append(
                    Code(
                        language=language,
                        content="\n".join(block),
                    )
                )

                continue

            #
            # Diagram
            #

            if token.value == "diagram":
                diagram_type = self._text_after(
                    tokens,
                    i,
                )

                block, i = self._collect_block(
                    tokens,
                    i + 2,
                    "diagram",
                )

                lesson.children.append(
                    Diagram(
                        diagram_type=diagram_type,
                        content="\n".join(block),
                    )
                )

                continue

            #
            # Image
            #

            if token.value == "image":
                lesson.children.append(
                    Image(
                        path=self._text_after(
                            tokens,
                            i,
                        )
                    )
                )

                i += 2
                continue

            #
            # Figure
            #

            if token.value == "figure":
                path = self._text_after(
                    tokens,
                    i,
                )

                block, i = self._collect_block(
                    tokens,
                    i + 2,
                    "figure",
                )

                lesson.children.append(
                    Figure(
                        path=path,
                        caption="\n".join(block),
                    )
                )

                continue

            #
            # Gallery
            #

            if token.value == "gallery":
                block, i = self._collect_block(
                    tokens,
                    i + 1,
                    "gallery",
                )

                lesson.children.append(
                    Gallery(
                        images=block,
                    )
                )

                continue

            #
            # References
            #

            if token.value == "references":
                block, i = self._collect_block(
                    tokens,
                    i + 1,
                    "references",
                )

                lesson.children.append(
                    References(
                        items=block,
                    )
                )

                continue

            #
            # Reading
            #

            if token.value == "reading":
                block, i = self._collect_block(
                    tokens,
                    i + 1,
                    "reading",
                )

                lesson.children.append(
                    Reading(
                        items=block,
                    )
                )

                continue

            #
            # Related
            #

            if token.value == "related":
                block, i = self._collect_block(
                    tokens,
                    i + 1,
                    "related",
                )

                lesson.children.append(
                    Related(
                        lessons=block,
                    )
                )

                continue

            #
            # Concepts
            #

            if token.value == "concepts":
                block, i = self._collect_block(
                    tokens,
                    i + 1,
                    "concepts",
                )

                lesson.children.append(
                    Concepts(
                        items=block,
                    )
                )

                continue

            #
            # Include
            #

            if token.value == "include":
                lesson.children.append(
                    Include(
                        path=self._text_after(
                            tokens,
                            i,
                        )
                    )
                )

                i += 2
                continue

            #
            # Snippet
            #

            if token.value == "snippet":
                name = self._text_after(
                    tokens,
                    i,
                )

                block, i = self._collect_block(
                    tokens,
                    i + 2,
                    "snippet",
                )

                lesson.children.append(
                    Snippet(
                        name=name,
                        content="\n".join(block),
                    )
                )

                continue

            #
            # Use
            #

            if token.value == "use":
                lesson.children.append(
                    Use(
                        name=self._text_after(
                            tokens,
                            i,
                        )
                    )
                )

                i += 2
                continue

            #
            # Navigation
            #

            if token.value == "next":
                lesson.children.append(
                    Next(
                        lesson=self._text_after(
                            tokens,
                            i,
                        )
                    )
                )

                i += 2
                continue

            if token.value == "previous":
                lesson.children.append(
                    Previous(
                        lesson=self._text_after(
                            tokens,
                            i,
                        )
                    )
                )

                i += 2
                continue

            #
            # Component
            #

            if token.value == "component":
                lesson.children.append(
                    Component(
                        name=self._text_after(
                            tokens,
                            i,
                        )
                    )
                )

                i += 2
                continue

            i += 1

        if lesson is None:
            raise ValueError("No lesson found.")

        return lesson

    def _text_after(
        self,
        tokens: list[Token],
        index: int,
    ) -> str:

        if (
            index + 1 < len(tokens)
            and tokens[index + 1].type == TokenType.TEXT
        ):
            return tokens[index + 1].value

        return ""

    def _collect_block(
        self,
        tokens: list[Token],
        start: int,
        directive: str,
    ) -> tuple[list[str], int]:

        lines = []

        i = start

        while i < len(tokens):
            token = tokens[i]

            if token.type == TokenType.DIRECTIVE and token.value == "end":
                return (
                    lines,
                    i + 1,
                )

            if token.type == TokenType.TEXT:
                lines.append(token.value)

            i += 1

        raise MissingEndDirectiveError(directive)
