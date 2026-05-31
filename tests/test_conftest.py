"""
tests.conftest
~~~~~~~~~~~~~~

Shared pytest fixtures for Point.

Provides reusable objects used across
parser, compiler, validator, and
pipeline tests.
"""

import pytest

from point.compiler.compiler import (
    MarkdownCompiler,
)
from point.parser.parser import (
    Parser,
)
from point.tokenizer.tokenizer import (
    Tokenizer,
)
from point.validators.validator import (
    Validator,
)


@pytest.fixture
def lesson_source():
    """
    Basic lesson source.
    """

    return """
@lesson Dependency Injection

@goals

- Understand DI
- Build container

@end

@warning

Avoid service locators.

@end
"""


@pytest.fixture
def tokenizer():
    """
    Tokenizer fixture.
    """

    return Tokenizer()


@pytest.fixture
def parser():
    """
    Parser fixture.
    """

    return Parser()


@pytest.fixture
def compiler():
    """
    Compiler fixture.
    """

    return MarkdownCompiler()


@pytest.fixture
def validator():
    """
    Validator fixture.
    """

    return Validator()


@pytest.fixture
def tokens(
    tokenizer,
    lesson_source,
):
    """
    Tokenized lesson.
    """

    return tokenizer.tokenize(lesson_source)


@pytest.fixture
def lesson(
    parser,
    tokens,
):
    """
    Parsed lesson AST.
    """

    return parser.parse(tokens)


@pytest.fixture
def markdown(
    compiler,
    lesson,
):
    """
    Compiled markdown.
    """

    return compiler.compile(lesson)
