"""
point.vitepress.generator
~~~~~~~~~~~~~~~~~~~~~~~~~

VitePress generation utilities.

Responsibilities
----------------

Generate VitePress configuration and supporting
site files for Point projects.

Features
--------

- index generation
- sidebar generation
- theme generation
- vitepress config generation
- glossary integration
- learning path integration
- knowledge graph integration
- GitHub Pages support
- custom styling support

Pipeline
--------

Point Project
      ↓

Generated Markdown
      ↓

VitePress Generator
      ↓

.vitepress/
      ↓

Static Documentation Site
"""

from pathlib import Path

from point.project.learning_path import (
    resolve_learning_path,
)

from point.project.manager import (
    ProjectManager,
)


def generate_index(
    docs_dir: Path,
) -> None:
    """
    Generate default home page.
    """

    content = """\
# Welcome

Built with Point.

## Start Learning

Use the sidebar to explore lessons and learning resources.

## Learning Resources

Point automatically generates:

- Glossary
- Learning Paths
- Knowledge Graph

## Features

- Structured lessons
- Educational concepts
- Definitions and terms
- Reusable content
- Knowledge relationships

## Next Steps

1. Open a lesson
2. Explore the glossary
3. Follow a learning path
4. Discover related concepts
"""

    (docs_dir / "index.md").write_text(
        content,
        encoding="utf-8",
    )


def generate_sidebar(
    project: ProjectManager,
) -> str:
    """
    Generate sidebar configuration.

    Parameters
    ----------
    docs_dir:
        Documentation directory.

    Returns
    -------
    str
        JavaScript sidebar object.
    """

    lessons = resolve_learning_path(
        project,
    )

    groups = {}
    section_order = []


    for lesson in lessons:
        relative = lesson.relative_to(
            project.lessons_dir,
        )
        
        relative = relative.with_suffix(
            ".md",
        )

        if len(relative.parts) > 1:
            section = (
                relative.parts[0].replace("-", " ").replace("_", " ").title()
            )

        else:
            section = "Lessons"

        if lesson.stem == "welcome":
            title = "Welcome"
            link = "/"
        else:
            title = (
                lesson.stem
                .replace("-", " ")
                .replace("_", " ")
                .title()
            )
        
            link = "/" + str(
                relative.with_suffix("")
            ).replace(
                "\\",
                "/",
            )

        if section not in groups:
            groups[section] = []
            section_order.append(section)
        
        groups[section].append(
            f"""{{
text: "{title}",
link: "{link}"
}}"""
        )
        
    sidebar_sections = []

    for section in section_order:
    
        items = groups[section]
        sidebar_sections.append(
            f"""{{
text: "{section}",
items: [
{",".join(items)}
]
}}"""
        )

    return f"""
[
{",".join(sidebar_sections)}
]
"""


def generate_theme(
    docs_dir: Path,
) -> None:
    """
    Generate Point VitePress theme.
    """

    theme_dir = docs_dir / ".vitepress" / "theme"

    theme_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    components_dir = theme_dir / "components"
    
    components_dir.mkdir(
        parents=True,
        exist_ok=True,
    )
    
    #
    # Custom CSS
    #

    (theme_dir / "custom.css").write_text(
        """
:root {

    --vp-c-brand-1: #9d00ff;
    --vp-c-brand-2: #b433ff;
    --vp-c-brand-3: #cb66ff;

    --vp-c-brand-soft: rgba(157, 0, 255, 0.15);
}

.point-definition,
.point-concept,
.point-theorem {

    margin: 1rem 0;
}

.point-learning-goals {

    padding: 1rem;
}

.point-summary {

    margin-top: 2rem;
}

.point-warning {

    margin: 1rem 0;
}

.point-note {

    margin: 1rem 0;
}

.point-tip {

    margin: 1rem 0;
}

.lesson-card {

    border-radius: 12px;
}
""".strip()
        + "\n",
        encoding="utf-8",
    )

    #
    # Theme Entry
    #

    (components_dir / "MermaidDiagram.vue").write_text(
    """
<script setup>
import mermaid from "mermaid"
import { onMounted, ref } from "vue"

const props = defineProps({
  chart: String,
})

const el = ref()

onMounted(async () => {
  mermaid.initialize({
    startOnLoad: false,

    flowchart: {
      useMaxWidth: false,
      htmlLabels: true,
    },
  })

  const id =
    `mermaid-${Math.random().toString(36).slice(2)}`

  const { svg } = await mermaid.render(
    id,
    props.chart,
  )

  el.value.innerHTML = svg

  const svgElement =
    el.value.querySelector("svg")

  if (svgElement) {
    svgElement.removeAttribute("width")
    svgElement.removeAttribute("height")

    svgElement.style.width = "100%"
    svgElement.style.height = "auto"
    svgElement.style.maxWidth = "none"
  }
})
</script>

<template>
  <div class="mermaid-wrapper">
    <div ref="el"></div>
  </div>
</template>

<style scoped>
.mermaid-wrapper {
  display: flex;
  justify-content: center;
  margin: 2rem 0;
  overflow-x: auto;
}

.mermaid-wrapper svg {
  min-width: 900px;
  height: auto;
}
</style>
    """.strip()
        + "\\n",
        encoding="utf-8",
    )
    
    (theme_dir / "index.ts").write_text(
        """
import DefaultTheme from "vitepress/theme"
import "./custom.css"

import MermaidDiagram from "./components/MermaidDiagram.vue"

export default {
  extends: DefaultTheme,

  enhanceApp({ app }) {
    app.component(
      "MermaidDiagram",
      MermaidDiagram,
    )
  },
}
    """.strip()
        + "\n",
        encoding="utf-8",
    )


def generate_config(
    title: str,
    docs_dir: Path,
    base: str = "/",
) -> None:
    """
    Generate VitePress configuration.

    Parameters
    ----------
    title:
        Site title.

    docs_dir:
        Documentation directory.

    base:
        Deployment base path.

    Examples
    --------

    Local:

        base="/"

    GitHub Pages:

        base="/learn-undreamt/"
    """

    vitepress_dir = docs_dir / ".vitepress"

    vitepress_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    project = ProjectManager()
    
    sidebar = generate_sidebar(
        project,
    )

    content = f"""\
import {{ defineConfig }} from "vitepress"

export default defineConfig({{

title: "{title}",

description:
"Generated by Point",

base: "{base}",

cleanUrls: true,

head: [
[
"meta",
{{
name: "generator",
content: "Point"
}}
]
],

themeConfig: {{

nav: [

{{
text: "Home",
link: "/"
}},

{{
text: "Glossary",
link: "/glossary/"
}},

{{
text: "Paths",
link: "/paths/"
}},

],

sidebar:
{sidebar}

}}

}})
"""

    (vitepress_dir / "config.mts").write_text(
        content,
        encoding="utf-8",
    )

    generate_theme(docs_dir)
