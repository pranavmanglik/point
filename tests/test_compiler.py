"""
tests.test_compiler
~~~~~~~~~~~~~~~~~~~

Compiler tests for Point.

Verifies that AST nodes are correctly
compiled into markdown output.
"""

from point.ast.nodes import (
    Code,
    Definition,
    Lesson,
    Note,
    Reading,
    References,
    Warning,
)
from point.compiler.compiler import (
    MarkdownCompiler,
)


def compile_lesson(
    lesson: Lesson,
) -> str:
    """
    Compile helper.
    """

    return MarkdownCompiler().compile(lesson)


def test_lesson_title():
    """
    Verify lesson title rendering.
    """

    lesson = Lesson(title="Dependency Injection")

    output = compile_lesson(lesson)

    assert "# Dependency Injection" in output


def test_warning_block():
    """
    Verify warning rendering.
    """

    lesson = Lesson(
        title="Intro",
        children=[Warning(content="Danger")],
    )

    output = compile_lesson(lesson)

    assert "::: warning" in output

    assert "Danger" in output


def test_note_block():
    """
    Verify note rendering.
    """

    lesson = Lesson(
        title="Intro",
        children=[Note(content="Remember this.")],
    )

    output = compile_lesson(lesson)

    assert "::: info" in output


def test_definition():
    """
    Verify definition rendering.
    """

    lesson = Lesson(
        title="Intro",
        children=[
            Definition(
                title="DI",
                content="Dependency Injection",
            )
        ],
    )

    output = compile_lesson(lesson)

    assert "DI" in output

    assert "Dependency Injection" in output


def test_code_block():
    """
    Verify code rendering.
    """

    lesson = Lesson(
        title="Intro",
        children=[
            Code(
                language="python",
                content='print("hello")',
            )
        ],
    )

    output = compile_lesson(lesson)

    assert "```python" in output

    assert 'print("hello")' in output


def test_references():
    """
    Verify references section.
    """

    lesson = Lesson(
        title="Intro",
        children=[
            References(
                items=[
                    "Clean Architecture",
                    "Design Patterns",
                ]
            )
        ],
    )

    output = compile_lesson(lesson)

    assert "## References" in output

    assert "Clean Architecture" in output


def test_reading():
    """
    Verify reading section.
    """

    lesson = Lesson(
        title="Intro",
        children=[Reading(items=["Martin Fowler"])],
    )

    output = compile_lesson(lesson)

    assert "Further Reading" in output

    assert "Martin Fowler" in output


def test_multiple_nodes():
    """
    Verify multiple nodes compile.
    """

    lesson = Lesson(
        title="Intro",
        children=[
            Note(content="Note"),
            Warning(content="Warning"),
            Code(
                language="python",
                content="print()",
            ),
        ],
    )

    output = compile_lesson(lesson)

    assert "Note" in output

    assert "Warning" in output

    assert "print()" in output
