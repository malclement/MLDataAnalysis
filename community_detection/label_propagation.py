import os
from typing import Dict

import networkx as nx

from community_detection.graph_utils import create_html_visualization
from community_detection.graph_utils import read_edges_with_ports_to_graph


def run_label_propagation(G: nx.Graph) -> Dict[str, int]:
    communities = nx.community.label_propagation_communities(G)
    partition = {}
    for i, community in enumerate(communities):
        for node in community:
            partition[node] = i
    return partition


def run(path: str):
    edges_file = os.path.join(os.getcwd(), path)
    G = read_edges_with_ports_to_graph(edges_file)
    partition = run_label_propagation(G)
    return {"Detected communities": partition}


def run_viz(path: str):
    edges_file = os.path.join(os.getcwd(), path)
    G = read_edges_with_ports_to_graph(edges_file)
    partition = run_label_propagation(G)
    return create_html_visualization(G=G, partition=partition)
