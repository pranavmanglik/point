"""
point.errors
~~~~~~~~~~~~

Exception hierarchy for Point.

Responsibilities
----------------

Provide structured exceptions for all
Point subsystems.

Features
--------

- parser errors
- compiler errors
- validation errors
- project errors

Overview
--------

All Point exceptions inherit from
PointError.

This allows applications and CLI
commands to catch Point-specific
failures using a single exception
type.
"""


class PointError(Exception):
    """
    Base exception for Point.

    All Point-specific exceptions
    inherit from this class.

    Example
    -------

    try:

        point_operation()

    except PointError as error:

        print(error)
    """


class PointParserError(
    PointError,
):
    """
    Base parser exception.

    Raised when an error occurs while
    converting tokens into an AST.

    Examples
    --------

    - missing @end
    - malformed block
    - invalid structure
    """


class PointCompilerError(
    PointError,
):
    """
    Base compiler exception.

    Raised when AST compilation
    fails.
    """


class PointValidationError(
    PointError,
):
    """
    Base validation exception.

    Raised when educational content
    violates validation rules.
    """


class PointProjectError(
    PointError,
):
    """
    Base project exception.

    Raised when project resources,
    configuration, or directories
    cannot be resolved.
    """


class MissingEndDirectiveError(
    PointParserError,
):
    """
    Missing @end directive.

    Raised when a block directive
    reaches end-of-file before
    a matching @end is found.
    """

    def __init__(
        self,
        directive: str,
    ):

        self.directive = directive

        super().__init__(f"Block '@{directive}' is missing @end.")
