import gzip

import networkx as nx


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
