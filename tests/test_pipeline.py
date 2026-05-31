"""
tests.test_pipeline
~~~~~~~~~~~~~~~~~~~

End-to-end pipeline tests for Point.

Verifies the complete compilation flow:

.point
   ↓
Tokenizer
   ↓
Parser
   ↓
Validator
   ↓
Compiler
   ↓
Markdown
"""

from point.compiler.compiler import (
    MarkdownCompiler,
)
from point.compiler.pipeline import (
    compile_file,
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


def test_full_pipeline():
    """
    Verify complete in-memory pipeline.
    """

    source = """
@lesson Dependency Injection

@goals

- Learn DI

@end

@warning

Avoid service locators.

@end
"""

    tokens = Tokenizer().tokenize(source)

    lesson = Parser().parse(tokens)

    errors = Validator().validate(lesson)

    assert errors == []

    markdown = MarkdownCompiler().compile(lesson)

    assert "# Dependency Injection" in markdown

    assert "Avoid service locators." in markdown


def test_compile_file(
    tmp_path,
):
    """
    Verify file compilation.
    """

    source_file = tmp_path / "intro.point"

    output_file = tmp_path / "intro.md"

    source_file.write_text(
        """
@lesson Intro

@note

Hello World

@end
""",
        encoding="utf-8",
    )

    compile_file(
        source_file,
        output_file,
    )

    assert output_file.exists()

    content = output_file.read_text(
        encoding="utf-8",
    )

    assert "# Intro" in content

    assert "Hello World" in content


def test_pipeline_with_code():
    """
    Verify code blocks survive pipeline.
    """

    source = """
@lesson Python

@code python

print("hello")

@end
"""

    tokens = Tokenizer().tokenize(source)

    lesson = Parser().parse(tokens)

    markdown = MarkdownCompiler().compile(lesson)

    assert "```python" in markdown

    assert 'print("hello")' in markdown


def test_pipeline_with_definition():
    """
    Verify educational blocks survive.
    """

    source = """
@lesson Intro

@definition Dependency Injection

Dependencies supplied externally.

@end
"""

    tokens = Tokenizer().tokenize(source)

    lesson = Parser().parse(tokens)

    markdown = MarkdownCompiler().compile(lesson)

    assert "Dependency Injection" in markdown


def test_pipeline_with_references():
    """
    Verify references compile.
    """

    source = """
@lesson Intro

@references

Clean Architecture
Design Patterns

@end
"""

    tokens = Tokenizer().tokenize(source)

    lesson = Parser().parse(tokens)

    markdown = MarkdownCompiler().compile(lesson)

    assert "References" in markdown

    assert "Clean Architecture" in markdown
