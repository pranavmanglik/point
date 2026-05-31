"""
point.ast.nodes
~~~~~~~~~~~~~~~

Abstract Syntax Tree (AST) node definitions
for Point.

The AST acts as the central document model
used throughout the compilation pipeline.

Pipeline
--------

.point
   ↓
Tokenizer
   ↓
Parser
   ↓
AST
   ↓
Compiler
   ↓
Markdown
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    List,
)

# ============================================================
# Base Node
# ============================================================


@dataclass(slots=True)
class Node:
    """
    Base AST node.
    """

    pass


# ============================================================
# Core
# ============================================================


@dataclass(slots=True)
class Lesson(Node):
    """
    Lesson document.
    """

    title: str

    children: List[Node] = field(default_factory=list)


@dataclass(slots=True)
class Meta(Node):
    """
    Lesson metadata.
    """

    values: dict[str, str]


@dataclass(slots=True)
class Section(Node):
    """
    Lesson section.
    """

    title: str

    content: str


@dataclass(slots=True)
class Goals(Node):
    """
    Learning goals.
    """

    items: list[str]


@dataclass(slots=True)
class Summary(Node):
    """
    Lesson summary.
    """

    content: str


# ============================================================
# Educational
# ============================================================


@dataclass(slots=True)
class Definition(Node):
    title: str

    content: str


@dataclass(slots=True)
class Term(Node):
    title: str

    content: str


@dataclass(slots=True)
class Concept(Node):
    title: str

    content: str


@dataclass(slots=True)
class Pitfall(Node):
    content: str


@dataclass(slots=True)
class BestPractice(Node):
    content: str


@dataclass(slots=True)
class Interview(Node):
    content: str


# ============================================================
# Content
# ============================================================


@dataclass(slots=True)
class Note(Node):
    content: str


@dataclass(slots=True)
class Tip(Node):
    content: str


@dataclass(slots=True)
class Warning(Node):
    content: str


@dataclass(slots=True)
class Danger(Node):
    content: str


@dataclass(slots=True)
class Info(Node):
    content: str


# ============================================================
# Code
# ============================================================


@dataclass(slots=True)
class Code(Node):
    language: str

    content: str


@dataclass(slots=True)
class CodeGroup(Node):
    blocks: list[Code]


# ============================================================
# Visual
# ============================================================


@dataclass(slots=True)
class Diagram(Node):
    diagram_type: str

    content: str


@dataclass(slots=True)
class Image(Node):
    path: str

    caption: str = ""


@dataclass(slots=True)
class Figure(Node):
    path: str

    caption: str = ""


@dataclass(slots=True)
class Gallery(Node):
    images: list[str]


# ============================================================
# Mathematics
# ============================================================


@dataclass(slots=True)
class Math(Node):
    content: str


@dataclass(slots=True)
class Equation(Node):
    content: str


@dataclass(slots=True)
class Theorem(Node):
    title: str

    content: str


# ============================================================
# Navigation
# ============================================================


@dataclass(slots=True)
class Next(Node):
    lesson: str


@dataclass(slots=True)
class Previous(Node):
    lesson: str


@dataclass(slots=True)
class Related(Node):
    lessons: list[str]


# ============================================================
# References
# ============================================================


@dataclass(slots=True)
class References(Node):
    items: list[str]


@dataclass(slots=True)
class Reading(Node):
    items: list[str]


# ============================================================
# Learning
# ============================================================


@dataclass(slots=True)
class Path(Node):
    title: str

    lessons: list[str]


@dataclass(slots=True)
class Concepts(Node):
    items: list[str]


# ============================================================
# Reusable Content
# ============================================================


@dataclass(slots=True)
class Include(Node):
    path: str


@dataclass(slots=True)
class Snippet(Node):
    name: str

    content: str


@dataclass(slots=True)
class Use(Node):
    name: str


# ============================================================
# Versioning
# ============================================================


@dataclass(slots=True)
class Version(Node):
    version: str

    children: List[Node] = field(default_factory=list)


# ============================================================
# Components
# ============================================================


@dataclass(slots=True)
class Component(Node):
    name: str

    props: dict[str, str] = field(default_factory=dict)
