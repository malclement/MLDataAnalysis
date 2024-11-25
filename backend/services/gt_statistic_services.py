from collections import Counter

import plotly.graph_objects as go
from fastapi.responses import HTMLResponse

from backend.services.gt_services import ground_truth_service
from backend.tools.custom_enums import FileSize


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

    _, gt_to_nodes = ground_truth_service(file_size=file_size)
    stats = ground_truth_statistics(gt_to_nodes)

    fig = plot_group_size_histogram(stats["histogram"])

    return HTMLResponse(content=fig.to_html(full_html=False), status_code=200)
