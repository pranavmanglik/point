"""
point.tokenizer.tokenizer
~~~~~~~~~~~~~~~~~~~~~~~~~

Tokenizer implementation for Point.

The tokenizer converts raw Point source text into
a stream of lexical tokens.

Responsibilities
----------------

The tokenizer is intentionally lightweight.

It is responsible only for:

- identifying directives
- extracting directive arguments
- preserving text content
- generating tokens

The tokenizer does NOT understand document
structure. All structural interpretation is
delegated to the parser.

Pipeline
--------

Point Source
      ↓

Tokenizer
      ↓

Tokens
      ↓

Parser
      ↓

AST

Examples
--------

Input:

    @lesson Dependency Injection

    @warning

    Avoid service locators.

    @end

Output:

    DIRECTIVE lesson
    TEXT Dependency Injection

    DIRECTIVE warning

    TEXT Avoid service locators.

    DIRECTIVE end
"""

from point.tokenizer.token import (
    Token,
    TokenType,
)


class Tokenizer:
    """
    Point source tokenizer.

    Converts raw Point source text into a sequence
    of tokens suitable for parsing.
    """

    def tokenize(
        self,
        content: str,
    ) -> list[Token]:
        """
        Convert Point source text into tokens.

        Parameters
        ----------
        content:
            Raw Point source.

        Returns
        -------
        list[Token]
            Generated token stream.
        """

        tokens: list[Token] = []

        for raw_line in content.splitlines():
            line = raw_line.rstrip()
        
            #
            # Ignore empty lines
            #
        
            if not line.strip():
                continue
        
            #
            # Ignore comments
            #
        
            if line.lstrip().startswith("#"):
                continue
            
            #
            # Directive
            #
            # Example:
            #
            #   @lesson Dependency Injection
            #
            # Produces:
            #
            #   DIRECTIVE lesson
            #   TEXT Dependency Injection
            #

            if line.startswith("@"):
                directive_line = line[1:]

                parts = directive_line.split(maxsplit=1)

                directive_name = parts[0].strip().lower()

                tokens.append(
                    Token(
                        type=TokenType.DIRECTIVE,
                        value=directive_name,
                    )
                )

                #
                # Directive argument
                #

                if len(parts) > 1:
                    argument = parts[1].strip()

                    if argument:
                        tokens.append(
                            Token(
                                type=TokenType.TEXT,
                                value=argument,
                            )
                        )

                continue

            #
            # Plain content
            #

            tokens.append(
                Token(
                    type=TokenType.TEXT,
                    value=line,
                )
            )

        return tokens
