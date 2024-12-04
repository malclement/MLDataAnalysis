import gzip
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import networkx as nx
import plotly.graph_objects as go


def read_edges_with_ports_to_graph(edges_file: str) -> nx.Graph:
    """
    Read edges from a file and create a NetworkX graph.
    """
    G = nx.Graph()
    with gzip.open(edges_file, mode="rt") as fopen:
        for line in fopen:
            if line.startswith("#"):  # Skip comment lines
                continue
            parts = line.split()
            if len(parts) < 3:
                continue
            node1, node2 = parts[1], parts[2]
            G.add_edge(node1, node2)
    return G


def create_html_visualization(
    G: nx.Graph,
    partition: Union[Dict[str, int], Tuple[List[str], ...]],
    title: str = "Network Visualization",
) -> str:
    """
    Create an HTML visualization of a NetworkX graph using Plotly.
    """
    # Determine positions for nodes
    pos = nx.spring_layout(G)

    # Create edge traces
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color="#888"),
        hoverinfo="none",
        mode="lines",
    )

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace["x"] += (x0, x1, None)
        edge_trace["y"] += (y0, y1, None)

    # Create node traces with color for communities
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode="markers",
        hoverinfo="text",
        marker=dict(
            showscale=True,
            colorscale="Viridis",
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title="Community",
                xanchor="left",
                titleside="right",
            ),
        ),
    )

    if isinstance(partition, dict):  # For algorithms like Louvain and Label Propagation
        for node in G.nodes():
            x, y = pos[node]
            node_trace["x"] += (x,)
            node_trace["y"] += (y,)
            # Color nodes by community
            node_trace["marker"]["color"] += (partition[node],)
            node_trace["text"] += (f"Node {node}<br>Community {partition[node]}",)
    else:  # For algorithms like Girvan-Newman
        node_to_community = {}
        for idx, community in enumerate(partition):
            for node in community:
                node_to_community[node] = idx

        for node in G.nodes():
            x, y = pos[node]
            node_trace["x"] += (x,)
            node_trace["y"] += (y,)
            # Color nodes by community
            node_trace["marker"]["color"] += (node_to_community[node],)
            node_trace["text"] += (
                f"Node {node}<br>Community {node_to_community[node]}",
            )

    # Build the figure
    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            title=title,
            titlefont_size=16,
            showlegend=False,
            hovermode="closest",
            margin=dict(l=0, r=0, b=0, t=40),
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
        ),
    )

    # Return the figure as an HTML string
    return fig.to_html(full_html=False)
