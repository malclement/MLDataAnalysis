import os
from typing import List
from typing import Tuple

import networkx as nx

from community_detection.graph_utils import create_html_visualization
from community_detection.graph_utils import read_edges_with_ports_to_graph


def run_girvan_newman(G: nx.Graph) -> Tuple[List[str], ...]:
    comp = nx.community.girvan_newman(G)
    communities = tuple(sorted(c) for c in next(comp))
    return communities


def run(path: str):
    edges_file = os.path.join(os.getcwd(), path)
    G = read_edges_with_ports_to_graph(edges_file)
    communities = run_girvan_newman(G)
    return {"Detected communities": communities}


def run_viz(path: str):
    edges_file = os.path.join(os.getcwd(), path)
    G = read_edges_with_ports_to_graph(edges_file)
    communities = run_girvan_newman(G)
    return create_html_visualization(G=G, partition=communities)
