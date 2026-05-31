# Point

> A language for building lessons, courses, and educational documentation.

Point is an educational authoring language that transforms structured learning content into complete learning experiences.

Write lessons using educational primitives such as definitions, concepts, learning goals, pitfalls, and learning paths — then generate documentation sites, glossaries, knowledge graphs, and reusable learning resources automatically.

---

## Why Point?

Most documentation systems are designed around pages.

Education is not just pages.

Teaching involves:

* learning goals
* concepts
* definitions
* prerequisites
* pitfalls
* practice
* progression

Traditional Markdown treats these as plain text.

Point treats them as first-class educational constructs.

This allows Point to understand your content and generate richer educational resources automatically.

---

## Example

```point
@lesson Dependency Injection

@goals

- Understand dependency injection
- Build a simple container
- Recognize common pitfalls

@end

@definition Dependency Injection

A design technique where dependencies are
provided from the outside rather than
created internally.

@end

@warning

Avoid using service locators as a substitute
for dependency injection.

@end

@summary

Dependency injection improves modularity,
testability, and maintainability.

@end
```

---

## What Point Generates

From a single lesson source, Point can generate:

### Documentation

* Markdown
* VitePress sites
* Course navigation
* Educational layouts

### Learning Resources

* Glossaries
* Learning paths
* Concept registries
* Snippet registries

### Knowledge Systems

* Knowledge graphs
* Concept relationships
* Cross-references
* Learning dependencies

---

## Educational Building Blocks

### Lesson Structure

```point
@lesson
@section
@goals
@summary
@meta
```

### Educational Content

```point
@definition
@concept
@term
@pitfall
@bestpractice
@interview
```

### Learning Aids

```point
@note
@tip
@warning
@danger
@info
```

### Visuals & Media

```point
@code
@diagram
@image
@figure
@gallery
```

### Mathematics

```point
@math
@equation
@theorem
```

### Navigation & Relationships

```point
@next
@previous
@related
@references
@reading
```

### Reusable Content

```point
@snippet
@use
@include
@component
```

---

## Installation

```bash
pip install point
```

---

## Quick Start

Create a course:

```bash
point init my-course
```

Create a lesson:

```bash
point create lesson intro
```

Build the course:

```bash
point build-all
```

Start the development server:

```bash
point serve
```

Create a production build:

```bash
point package
```

---

## Project Structure

```text
my-course/

├── lessons/
│   └── intro.point
│
├── docs/
│   ├── intro.md
│   └── .vitepress/
│
├── assets/
├── components/
│
├── package.json
└── point.toml
```

---

## Compilation Pipeline

```text
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
    ↓
VitePress
    ↓
Static Learning Site
```

---

## Philosophy

Point is not a documentation generator.

Point is an educational authoring system.

Documentation is one of its outputs.

The goal is to give educators, developers, and course creators a language that understands teaching as a first-class concern.

---

## License

MIT
