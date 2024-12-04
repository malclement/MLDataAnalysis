import gzip

import networkx as nx
import plotly.graph_objects as go

from backend.tools.custom_enums import FileSize
from backend.tools.path_selecter import path_selecter


def parse_small_path(file_path):
    """
    Parse edge data from the 'small_path' file.
    Each line specifies graph ID, client node, server node, and optional port info.

    Parameters:
    - file_path: Path to the gzip file containing edge data.

    Returns:
    - G: A NetworkX graph object representing the network.
    """
    G = nx.Graph()

    with gzip.open(file_path, mode="rt") as file:
        for line in file:
            if line.startswith("#"):
                continue  # Skip comment lines
            parts = line.strip().split()
            if len(parts) < 4:
                continue  # Skip incomplete lines

            graph_id, client, server, port_info = parts[0], parts[1], parts[2], parts[3]

            # Add nodes and edges to the graph
            G.add_node(client)
            G.add_node(server)
            G.add_edge(client, server, port_info=port_info)

    return G


def visualize_network_from_file(file_path, title="Small Path Network Visualization"):
    """
    Parse and visualize the network from a file like 'small_path'.

    Parameters:
    - file_path: Path to the gzip file containing edge data.
    - title: Title for the visualization.

    Returns:
    - fig: A Plotly figure object.
    """
    # Parse the edge data and build the graph
    G = parse_small_path(file_path)

    # Generate positions for the nodes
    pos = nx.spring_layout(G, seed=42)

    # Prepare edge traces
    edge_x, edge_y, edge_hover = [], [], []
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_hover.append(f"{edge[0]} ↔ {edge[1]}: {edge[2].get('port_info', 'N/A')}")

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color="gray"),
        hoverinfo="text",
        text=edge_hover,
        mode="lines",
    )

    # Prepare node traces
    node_x, node_y, node_text = [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        degree = G.degree[node]
        node_text.append(f"Node: {node}, Degree: {degree}")

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        text=node_text,
        marker=dict(
            showscale=True,
            colorscale="YlGnBu",
            size=10,
            colorbar=dict(
                thickness=15, title="Node Degree", xanchor="left", titleside="right"
            ),
            color=[G.degree[node] for node in G.nodes()],
        ),
    )

    # Create the figure
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

    # Return the figure as an HTML string for FastAPI to handle
    return fig.to_html(full_html=False)


def visualization_service(file_size: FileSize):
    file_path = path_selecter(file_size=file_size)

    fig = visualize_network_from_file(file_path)

    return fig
