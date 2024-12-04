import os
from typing import Dict

import networkx as nx

from community_detection.graph_utils import create_html_visualization
from community_detection.graph_utils import read_edges_with_ports_to_graph


def run_louvain(G: nx.Graph) -> Dict[str, int]:
    partition = nx.community.louvain_communities(G)
    node_community_map = {}
    for community_id, nodes in enumerate(partition):
        for node in nodes:
            node_community_map[node] = community_id
    return node_community_map


def run(path: str):
    edges_file = os.path.join(os.getcwd(), path)
    G = read_edges_with_ports_to_graph(edges_file)
    partition = run_louvain(G)
    return {"Detected communities": partition}


def run_viz(path: str):
    edges_file = os.path.join(os.getcwd(), path)
    G = read_edges_with_ports_to_graph(edges_file)
    partition = run_louvain(G)
    return create_html_visualization(G=G, partition=partition)
