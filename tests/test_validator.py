"""
tests.test_validator
~~~~~~~~~~~~~~~~~~~~

Validator tests for Point.

Verifies that AST validation catches
invalid educational content.
"""

from point.ast.nodes import (
    Code,
    Goals,
    Lesson,
    References,
    Snippet,
)
from point.validators.validator import (
    Validator,
)


def test_valid_lesson():
    """
    Valid lesson should pass.
    """

    lesson = Lesson(
        title="Dependency Injection",
    )

    errors = Validator().validate(lesson)

    assert errors == []


def test_missing_title():
    """
    Lesson title is required.
    """

    lesson = Lesson(
        title="",
    )

    errors = Validator().validate(lesson)

    assert len(errors) > 0


def test_empty_goals():
    """
    Goals cannot be empty.
    """

    lesson = Lesson(
        title="Intro",
        children=[Goals(items=[])],
    )

    errors = Validator().validate(lesson)

    assert len(errors) > 0


def test_valid_goals():
    """
    Goals should validate.
    """

    lesson = Lesson(
        title="Intro",
        children=[Goals(items=["Learn DI"])],
    )

    errors = Validator().validate(lesson)

    assert errors == []


def test_empty_code_language():
    """
    Code language required.
    """

    lesson = Lesson(
        title="Intro",
        children=[
            Code(
                language="",
                content="print()",
            )
        ],
    )

    errors = Validator().validate(lesson)

    assert len(errors) > 0


def test_empty_code_content():
    """
    Code content required.
    """

    lesson = Lesson(
        title="Intro",
        children=[
            Code(
                language="python",
                content="",
            )
        ],
    )

    errors = Validator().validate(lesson)

    assert len(errors) > 0


def test_empty_snippet_name():
    """
    Snippet name required.
    """

    lesson = Lesson(
        title="Intro",
        children=[
            Snippet(
                name="",
                content="Hello",
            )
        ],
    )

    errors = Validator().validate(lesson)

    assert len(errors) > 0


def test_empty_snippet_content():
    """
    Snippet content required.
    """

    lesson = Lesson(
        title="Intro",
        children=[
            Snippet(
                name="hello",
                content="",
            )
        ],
    )

    errors = Validator().validate(lesson)

    assert len(errors) > 0


def test_empty_references():
    """
    References cannot be empty.
    """

    lesson = Lesson(
        title="Intro",
        children=[References(items=[])],
    )

    errors = Validator().validate(lesson)

    assert len(errors) > 0


def test_valid_references():
    """
    References should validate.
    """

    lesson = Lesson(
        title="Intro",
        children=[References(items=["Clean Architecture"])],
    )

    errors = Validator().validate(lesson)

    assert errors == []
