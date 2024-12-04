import gzip
import os
import random
from typing import List
from typing import Tuple

import networkx as nx
import plotly.graph_objects as go


def read_edges_with_ports_to_graph(edges_file: str) -> nx.Graph:
    G = nx.Graph()
    with gzip.open(edges_file, mode="rt") as fopen:
        for line in fopen:
            if line.startswith("#"):  # skip comment lines
                continue
            parts = line.split()
            if len(parts) < 3:
                continue
            node1, node2 = parts[1], parts[2]
            G.add_edge(node1, node2)
    return G


def run_girvan_newman(G: nx.Graph) -> Tuple[List[str], ...]:
    comp = nx.community.girvan_newman(G)
    communities = tuple(sorted(c) for c in next(comp))
    return communities


def create_html_visualization(
    G: nx.Graph,
    communities: Tuple[List[str], ...],
    title: str = "Network with Girvan-Newman Communities",
) -> str:
    # Node positions for visualization
    pos = nx.spring_layout(G)

    # Create edge trace for visualization
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

    # Create node trace with color for communities
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

    # Assign nodes to communities and color them
    node_to_community = {}
    for idx, community in enumerate(communities):
        for node in community:
            node_to_community[node] = idx

    for node in G.nodes():
        x, y = pos[node]
        node_trace["x"] += (x,)
        node_trace["y"] += (y,)
        # Color nodes by their community
        node_trace["marker"]["color"] += (node_to_community[node],)
        node_trace["text"] += (f"Node {node}<br>Community {node_to_community[node]}",)

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


if __name__ == "__main__":
    # Specify the edges file location
    edges_file = os.path.join(
        os.getcwd(),
        "Cisco_22_networks/dir_g21_small_workload_with_gt/dir_no_packets_etc/edges_2days_feb10thruFeb11_all_49sensors.csv.txt.gz",
    )

    G = read_edges_with_ports_to_graph(edges_file)

    communities = run_girvan_newman(G)
    print(f"Detected communities: {communities}")

    html_output = create_html_visualization(G=G, communities=communities)
    with open("network_visualization.html", "w") as f:
        f.write(html_output)


def run(path: str):
    edges_file = os.path.join(
        os.getcwd(),
        path,
    )

    G = read_edges_with_ports_to_graph(edges_file)

    communities = run_girvan_newman(G)

    return {"Detected communities": communities}


def run_viz(path: str):
    edges_file = os.path.join(
        os.getcwd(),
        path,
    )

    G = read_edges_with_ports_to_graph(edges_file)

    communities = run_girvan_newman(G)

    html_output = create_html_visualization(G=G, communities=communities)
    return html_output
