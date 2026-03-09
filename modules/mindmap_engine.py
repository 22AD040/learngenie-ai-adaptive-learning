import re


def extract_sections(content):

    sections = []

    lines = content.split("\n")

    for line in lines:

        line = line.strip()

        if line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4.") or line.startswith("5."):
            sections.append(line.replace("*", ""))

        elif ":" in line and len(line) < 80:
            sections.append(line.replace("*", ""))

    return sections[:6]


def extract_points(content):

    points = []

    lines = content.split("\n")

    for line in lines:

        line = line.strip()

        if line.startswith("-") or line.startswith("•") or line.startswith("*"):

            clean = line.replace("-", "").replace("•", "").replace("*", "").strip()

            if len(clean) > 5:
                points.append(clean)

    return points[:10]


def generate_mindmap(topic, content):

    sections = extract_sections(content)
    points = extract_points(content)

    graph = f"""
    digraph MindMap {{

    rankdir=TB
    size="10,8"
    nodesep=1.0
    ranksep=1.2

    node [
        shape=box
        style=filled
        fontname=Helvetica
        fontsize=14
        width=2.5
    ]

    Topic [
        label="{topic}"
        shape=ellipse
        fillcolor="#3b82f6"
        fontcolor="white"
        fontsize=18
    ]

    """

    p_index = 0

    for i, sec in enumerate(sections):

        node = f"section{i}"

        graph += f'{node} [label="{sec}" fillcolor="#86efac"]\n'
        graph += f"Topic -> {node}\n"

        for j in range(2):

            if p_index >= len(points):
                break

            point = points[p_index]
            p_index += 1

            pnode = f"{node}_p{j}"

            graph += f'{pnode} [label="{point}" fillcolor="#fde68a"]\n'
            graph += f"{node} -> {pnode}\n"

    graph += "}"

    return graph


def generate_mindmap_explanation(topic, content):

    sections = extract_sections(content)

    explanation = f"""
    This mind map provides a visual overview of the topic **{topic}**.

    The central node represents the main concept. From it, major sections branch out,
    highlighting the key ideas related to the topic.

    """

    if sections:

        explanation += "The main concepts included in this mind map are:\n\n"

        for sec in sections[:5]:
            explanation += f"- {sec}\n"

    explanation += """

    Each section may further branch into smaller points that explain the concept
    in more detail. This structure helps learners quickly understand how the ideas
    are connected and improves memory retention.

    """

    return explanation