import os
import random
from typing import Dict

import networkx as nx
import plotly.graph_objects as go

from community_detection import read_edges_with_ports_to_graph


def run_louvain(G: nx.Graph) -> Dict[str, int]:
    # Using Louvain algorithm to partition the graph into communities
    partition = nx.community.louvain_communities(G)
    node_community_map = {}
    for community_id, nodes in enumerate(partition):
        for node in nodes:
            node_community_map[node] = community_id
    return node_community_map


def create_html_visualization(
    G: nx.Graph,
    partition: Dict[str, int],
    title: str = "Network with Louvain Communities",
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

    for node in G.nodes():
        x, y = pos[node]
        node_trace["x"] += (x,)
        node_trace["y"] += (y,)
        # Color nodes by their community
        node_trace["marker"]["color"] += (partition[node],)
        node_trace["text"] += (f"Node {node}<br>Community {partition[node]}",)

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

    # Return the figure as an HTML string for FastAPI to handle
    return fig.to_html(full_html=False)


if __name__ == "__main__":
    # Specify the edges file location
    edges_file = os.path.join(
        os.getcwd(),
        "Cisco_22_networks/dir_g21_small_workload_with_gt/dir_no_packets_etc/edges_2days_feb10thruFeb11_all_49sensors.csv.txt.gz",
    )

    G = read_edges_with_ports_to_graph(edges_file)

    partition = run_louvain(G)
    print(f"Detected communities: {partition}")

    html_output = create_html_visualization(G=G, partition=partition)
    with open("network_visualization.html", "w") as f:
        f.write(html_output)


def run(path: str):
    edges_file = os.path.join(
        os.getcwd(),
        path,
    )

    G = read_edges_with_ports_to_graph(edges_file=edges_file)

    partition = run_louvain(G)

    return {"Detected communities": partition}


def run_viz(path: str):
    edges_file = os.path.join(
        os.getcwd(),
        path,
    )

    G = read_edges_with_ports_to_graph(edges_file=edges_file)

    partition = run_louvain(G)

    html_output = create_html_visualization(G=G, partition=partition)
    return html_output
