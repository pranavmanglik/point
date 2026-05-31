"""
tests.run_pipeline
~~~~~~~~~~~~~~~~~~

Manual pipeline runner for Point.

Purpose
-------

Verify the complete Point pipeline:

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

This script is intended for development and
debugging only.

Eventually most behavior should be covered by
pytest test cases.
"""

from pathlib import Path

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


def main() -> None:

    source_path = Path("examples/di.point")

    content = source_path.read_text(encoding="utf-8")

    print("\n--- SOURCE ---\n")

    print(content)

    #
    # Tokenize
    #

    tokens = Tokenizer().tokenize(content)

    print("\n--- TOKENS ---\n")

    for token in tokens:
        print(token)

    #
    # Parse
    #

    lesson = Parser().parse(tokens)

    print("\n--- AST ---\n")

    print(lesson)

    #
    # Validate
    #

    errors = Validator().validate(lesson)

    print("\n--- VALIDATION ---\n")

    if errors:
        for error in errors:
            print(error)

        return

    print("Validation passed.")

    #
    # Compile
    #

    markdown = MarkdownCompiler().compile(lesson)

    print("\n--- MARKDOWN ---\n")

    print(markdown)


if __name__ == "__main__":
    main()
