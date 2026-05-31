"""
point.validators.validator
~~~~~~~~~~~~~~~~~~~~~~~~~~

Validation system for Point.

The validator operates on the AST produced by the parser
and ensures Point documents satisfy language rules before
compilation.

Validation Categories
---------------------

- document validation
- metadata validation
- educational content validation
- code validation
- navigation validation
- resource validation

The validator should never modify the AST.

Its sole responsibility is reporting problems.
"""

from dataclasses import dataclass

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


@dataclass(slots=True)
class ValidationError:
    """
    Represents a validation issue.
    """

    message: str

    def __str__(self) -> str:
        return self.message


class Validator:
    """
    Point AST validator.
    """

    def validate(
        self,
        lesson: Lesson,
    ) -> list[ValidationError]:
        """
        Validate a lesson AST.
        """

        errors: list[ValidationError] = []

        #
        # Lesson
        #

        if not lesson.title.strip():
            errors.append(ValidationError("Lesson title is required."))

        #
        # Children
        #

        for node in lesson.children:
            self._validate_node(
                node,
                errors,
            )

        return errors

    def _validate_node(
        self,
        node,
        errors: list[ValidationError],
    ) -> None:
        """
        Validate a single node.
        """

        #
        # Meta
        #

        if isinstance(
            node,
            Meta,
        ):
            if not node.values:
                errors.append(ValidationError("Meta block cannot be empty."))

        #
        # Goals
        #

        elif isinstance(
            node,
            Goals,
        ):
            if not node.items:
                errors.append(ValidationError("Goals cannot be empty."))

        #
        # Generic Content Blocks
        #

        elif isinstance(
            node,
            (
                Note,
                Tip,
                Warning,
                Danger,
                Info,
                Pitfall,
                BestPractice,
                Interview,
                Summary,
                Math,
                Equation,
            ),
        ):
            if not node.content.strip():
                errors.append(
                    ValidationError(
                        f"{node.__class__.__name__} cannot be empty."
                    )
                )

        #
        # Educational Blocks
        #

        elif isinstance(
            node,
            (
                Definition,
                Term,
                Concept,
                Theorem,
            ),
        ):
            if not node.title.strip():
                errors.append(
                    ValidationError(
                        f"{node.__class__.__name__} title missing."
                    )
                )

            if not node.content.strip():
                errors.append(
                    ValidationError(
                        f"{node.__class__.__name__} content missing."
                    )
                )

        #
        # Section
        #

        elif isinstance(
            node,
            Section,
        ):
            if not node.title.strip():
                errors.append(ValidationError("Section title missing."))

            if not node.content.strip():
                errors.append(ValidationError("Section content missing."))

        #
        # Code
        #

        elif isinstance(
            node,
            Code,
        ):
            if not node.language.strip():
                errors.append(ValidationError("Code language missing."))

            if not node.content.strip():
                errors.append(ValidationError("Code block is empty."))

        #
        # Diagram
        #

        elif isinstance(
            node,
            Diagram,
        ):
            if not node.diagram_type.strip():
                errors.append(ValidationError("Diagram type missing."))

            if not node.content.strip():
                errors.append(ValidationError("Diagram content missing."))

        #
        # Images
        #

        elif isinstance(
            node,
            (
                Image,
                Figure,
            ),
        ):
            if not node.path.strip():
                errors.append(
                    ValidationError(f"{node.__class__.__name__} path missing.")
                )

        #
        # Gallery
        #

        elif isinstance(
            node,
            Gallery,
        ):
            for image in node.images:
                if not image.strip():
                    errors.append(
                        ValidationError("Gallery contains empty image path.")
                    )

        #
        # Navigation
        #

        elif isinstance(
            node,
            (
                Next,
                Previous,
            ),
        ):
            if not node.lesson.strip():
                errors.append(
                    ValidationError(
                        f"{node.__class__.__name__} lesson missing."
                    )
                )

        elif isinstance(
            node,
            Related,
        ):
            if not node.lessons:
                errors.append(
                    ValidationError("Related lessons cannot be empty.")
                )

        #
        # References
        #

        elif isinstance(
            node,
            (
                References,
                Reading,
            ),
        ):
            if not node.items:
                errors.append(
                    ValidationError(
                        f"{node.__class__.__name__} cannot be empty."
                    )
                )

            for item in node.items:
                if not item.strip():
                    errors.append(
                        ValidationError(
                            f"{node.__class__.__name__} contains empty item."
                        )
                    )

        #
        # Learning Paths
        #

        elif isinstance(
            node,
            Path,
        ):
            if not node.title.strip():
                errors.append(ValidationError("Path title missing."))

            if not node.lessons:
                errors.append(ValidationError("Path requires lessons."))

        #
        # Knowledge Graph
        #

        elif isinstance(
            node,
            Concepts,
        ):
            if not node.items:
                errors.append(ValidationError("Concept list cannot be empty."))

        #
        # Reusable Content
        #

        elif isinstance(
            node,
            Include,
        ):
            if not node.path.strip():
                errors.append(ValidationError("Include path missing."))

        elif isinstance(
            node,
            Snippet,
        ):
            if not node.name.strip():
                errors.append(ValidationError("Snippet name missing."))

            if not node.content.strip():
                errors.append(ValidationError("Snippet content missing."))

        elif isinstance(
            node,
            Use,
        ):
            if not node.name.strip():
                errors.append(ValidationError("Snippet name missing."))

        #
        # Version
        #

        elif isinstance(
            node,
            Version,
        ):
            if not node.version.strip():
                errors.append(ValidationError("Version identifier missing."))

        #
        # Components
        #

        elif isinstance(
            node,
            Component,
        ):
            if not node.name.strip():
                errors.append(ValidationError("Component name missing."))
