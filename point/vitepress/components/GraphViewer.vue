<script setup>
import { ref, onMounted } from "vue"
import cytoscape from "cytoscape"

const graph = ref(null)

onMounted(async () => {

    const response = await fetch(
        "/graph/graph.json"
    )

    graph.value = await response.json()

    const elements = [

        ...graph.value.nodes.map(
            node => ({
                data: {
                    id: node.id,
                    label: node.label,
                    type: node.type,
                }
            })
        ),

        ...graph.value.edges.map(
            edge => ({
                data: {
                    source: edge.source,
                    target: edge.target,
                }
            })
        ),
    ]

    cytoscape({

        container:
            document.getElementById(
                "graph"
            ),

        elements,

        layout: {
            name: "cose",
        },
    })
})
</script>

<template>

<div>

<div
    id="graph"
    style="
        width: 100%;
        height: 600px;
        border: 1px solid #ddd;
    "
></div>

</div>

</template>
