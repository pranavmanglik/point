"""
tests.test_parser
~~~~~~~~~~~~~~~~~

Parser tests for Point.

Verifies that token streams are correctly
converted into AST structures.
"""

from point.ast.nodes import (
    Code,
    Definition,
    Goals,
    Lesson,
    Path,
    Snippet,
    Use,
    Warning,
)
from point.parser.parser import (
    Parser,
)
from point.tokenizer.tokenizer import (
    Tokenizer,
)


def parse(
    source: str,
):
    """
    Helper parser.
    """

    tokens = Tokenizer().tokenize(source)

    return Parser().parse(tokens)


def test_lesson():
    """
    Verify lesson parsing.
    """

    lesson = parse(
        """
@lesson Dependency Injection
"""
    )

    assert isinstance(
        lesson,
        Lesson,
    )

    assert lesson.title == "Dependency Injection"


def test_goals():
    """
    Verify goals parsing.
    """

    lesson = parse(
        """
@lesson Intro

@goals

- Learn DI
- Build Container

@end
"""
    )

    goals = lesson.children[0]

    assert isinstance(
        goals,
        Goals,
    )

    assert len(goals.items) == 2


def test_warning():
    """
    Verify warning parsing.
    """

    lesson = parse(
        """
@lesson Intro

@warning

Danger.

@end
"""
    )

    node = lesson.children[0]

    assert isinstance(
        node,
        Warning,
    )

    assert node.content == "Danger."


def test_definition():
    """
    Verify definition parsing.
    """

    lesson = parse(
        """
@lesson Intro

@definition Dependency Injection

Dependencies are supplied externally.

@end
"""
    )

    node = lesson.children[0]

    assert isinstance(
        node,
        Definition,
    )

    assert node.title == "Dependency Injection"


def test_code():
    """
    Verify code block parsing.
    """

    lesson = parse(
        """
@lesson Intro

@code python

print("hello")

@end
"""
    )

    node = lesson.children[0]

    assert isinstance(
        node,
        Code,
    )

    assert node.language == "python"

    assert "print" in node.content


def test_snippet():
    """
    Verify snippet parsing.
    """

    lesson = parse(
        """
@lesson Intro

@snippet greeting

Hello World

@end
"""
    )

    node = lesson.children[0]

    assert isinstance(
        node,
        Snippet,
    )

    assert node.name == "greeting"

    assert node.content == "Hello World"


def test_use():
    """
    Verify snippet usage parsing.
    """

    lesson = parse(
        """
@lesson Intro

@use greeting
"""
    )

    node = lesson.children[0]

    assert isinstance(
        node,
        Use,
    )

    assert node.name == "greeting"


def test_path():
    """
    Verify learning path parsing.
    """

    lesson = parse(
        """
@lesson Intro

@path Backend

HTTP
REST
Auth

@end
"""
    )

    node = lesson.children[0]

    assert isinstance(
        node,
        Path,
    )

    assert node.title == "Backend"

    assert len(node.lessons) == 3


def test_missing_lesson():
    """
    Lesson must exist.
    """

    tokens = Tokenizer().tokenize(
        """
@warning

Danger

@end
"""
    )

    try:
        Parser().parse(tokens)

        assert False

    except ValueError:
        assert True
