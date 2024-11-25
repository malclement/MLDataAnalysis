import gzip
import os
from collections import Counter
from collections import defaultdict

import networkx as nx
import plotly.graph_objects as go
import plotly.io as pio
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse

from backend.tools.custom_enums import FileSize
from backend.tools.path_selecter import path_selecter


def ground_truth_service(file_size: FileSize):
    """
    This function reads a ground truth file (including gzipped files) and returns two mappings:
    1. node_gt: A dictionary mapping node ID to group ID.
    2. gt_to_nodes: A dictionary mapping group ID to a set of nodes in that group.

    Parameters:
    - gt_file: Path to the ground truth file.

    Returns:
    - node_gt: Dictionary mapping node to group ID.
    - gt_to_nodes: Dictionary mapping group ID to set of nodes.
    """
    gt_file = path_selecter(file_size=file_size)
    node_gt = {}
    gt_to_nodes = defaultdict(set)

    if gt_file.endswith(".gz"):
        with gzip.open(gt_file, "rt", encoding="utf-8") as f:
            group_id = 0

            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                group_id += 1
                parts = line.split(",")

                for node_id in parts:
                    node_gt[node_id] = group_id
                    gt_to_nodes[group_id].add(node_id)
    else:
        with open(gt_file, "r", encoding="utf-8") as f:
            group_id = 0
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                group_id += 1
                parts = line.split(",")

                for node_id in parts:
                    node_gt[node_id] = group_id
                    gt_to_nodes[group_id].add(node_id)

    return node_gt, gt_to_nodes


def ground_truth_visualization(node_gt, gt_to_nodes):
    """
    Visualizes the ground truth data as a graph using Plotly and NetworkX.

    Parameters:
    - node_gt: Dictionary mapping node to group ID.
    - gt_to_nodes: Dictionary mapping group ID to set of nodes.

    Returns:
    - HTMLResponse: Plotly visualization embedded in HTML.
    """
    # Create a graph using NetworkX
    G = nx.Graph()

    # Add nodes and edges to the graph
    for group_id, nodes in gt_to_nodes.items():
        nodes_list = list(nodes)
        # Add edges for nodes within the same group
        for i in range(len(nodes_list)):
            for j in range(i + 1, len(nodes_list)):
                # Clean node names before adding them as edges
                node_1 = nodes_list[i].strip()  # Ensure no extra spaces or tabs
                node_2 = nodes_list[j].strip()
                G.add_edge(node_1, node_2)

        # Add node attributes (group_id) after sanitizing the node names
        for node in nodes_list:
            sanitized_node = node.strip()  # Clean the node ID
            G.add_node(
                sanitized_node, group=group_id
            )  # Add sanitized node with its group ID

    # Generate node positions using spring layout
    pos = nx.spring_layout(G, seed=42)  # Ensuring reproducibility

    # Create edge traces
    edge_trace = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace.append(
            go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                line=dict(width=0.5, color="gray"),
                hoverinfo="none",
                mode="lines",
            )
        )

    # Create node traces
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode="markers",
        hoverinfo="text",
        marker=dict(
            showscale=True,
            colorscale="YlGnBu",
            size=10,
            colorbar=dict(
                thickness=15, title="Group ID", xanchor="left", titleside="right"
            ),
        ),
    )

    # Prepare the node trace data
    node_trace_x = []
    node_trace_y = []
    node_trace_text = []
    node_trace_color = []

    for node in G.nodes():
        x, y = pos[node]
        node_trace_x.append(x)
        node_trace_y.append(y)
        node_trace_text.append(f"Node: {node}, Group: {G.nodes[node]['group']}")
        node_trace_color.append(G.nodes[node]["group"])

    # Set the trace data
    node_trace["x"] = node_trace_x
    node_trace["y"] = node_trace_y
    node_trace["text"] = node_trace_text
    node_trace.marker.color = node_trace_color

    # Create the figure
    fig = go.Figure(
        data=edge_trace + [node_trace],
        layout=go.Layout(
            title="Network Visualization",
            titlefont_size=16,
            showlegend=False,
            hovermode="closest",
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
            margin=dict(l=0, r=0, b=0, t=0),
        ),
    )

    return HTMLResponse(content=fig.to_html(full_html=False), status_code=200)


OUTPUT_FOLDER = ""


def ground_truth_visualization_service(
    file_size: FileSize = FileSize.SMALL, save: bool = False
):
    node_gt, gt_to_nodes = ground_truth_service(file_size=file_size)
    fig = ground_truth_visualization(node_gt=node_gt, gt_to_nodes=gt_to_nodes)

    # Save the figure as an image if requested
    if save:
        image_filename = "ground_truth_visualization.png"
        image_path = os.path.join(OUTPUT_FOLDER, image_filename)

        # Save the image
        pio.write_image(fig, image_path)

        # Return the image file as a downloadable response
        return FileResponse(image_path, media_type="image/png", filename=image_filename)

    # Otherwise, render the Plotly figure as HTML content
    return HTMLResponse(fig)


def ground_truth_statistics(gt_to_nodes):
    """
    Computes statistics for ground truth data, including:
    - Number of groups.
    - Size of each group.
    - Histogram of group sizes.

    Parameters:
    - gt_to_nodes: Dictionary mapping group ID to set of nodes.

    Returns:
    - stats: Dictionary containing number of groups, group sizes, and histogram.
    """
    num_groups = len(gt_to_nodes)

    group_sizes = {group_id: len(nodes) for group_id, nodes in gt_to_nodes.items()}

    histogram = Counter(group_sizes.values())

    stats = {
        "num_groups": num_groups,
        "group_sizes": group_sizes,
        "histogram": histogram,
    }

    return stats


def ground_truth_statistics_service(file_size: FileSize):
    """
    Reads ground truth data, computes and returns statistics.
    """
    _, gt_to_nodes = ground_truth_service(file_size=file_size)
    return ground_truth_statistics(gt_to_nodes)


def plot_group_size_histogram(histogram, title="Histogram of Group Sizes"):
    """
    Creates a histogram visualization of group sizes.

    Parameters:
    - histogram: A Counter object representing the frequency of group sizes.
    - title: The title for the plot.

    Returns:
    - fig: A Plotly figure object.
    """
    group_sizes = list(histogram.keys())
    frequencies = list(histogram.values())

    fig = go.Figure(
        data=[
            go.Bar(x=group_sizes, y=frequencies, text=frequencies, textposition="auto")
        ],
        layout=go.Layout(
            title=title,
            xaxis=dict(title="Group Size"),
            yaxis=dict(title="Frequency"),
            bargap=0.2,
        ),
    )

    return fig


def display_histogram_service(file_size: FileSize):
    """
    Reads ground truth data, computes statistics, and returns a histogram visualization.
    """

    node_gt, gt_to_nodes = ground_truth_service(file_size=file_size)
    stats = ground_truth_statistics(gt_to_nodes)

    fig = plot_group_size_histogram(stats["histogram"])

    return HTMLResponse(content=fig.to_html(full_html=False), status_code=200)
