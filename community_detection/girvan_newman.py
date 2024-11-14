import gzip
import os
import random
from typing import List
from typing import Tuple

import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.community import girvan_newman


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
    comp = girvan_newman(G)
    communities = tuple(sorted(c) for c in next(comp))
    return communities


def draw_communities(G: nx.Graph, communities: Tuple[List[str], ...]):
    pos = nx.spring_layout(G)  # Positioning for nodes

    colors = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(len(communities))]
    plt.figure(figsize=(10, 10))

    for idx, community in enumerate(communities):
        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=community,
            node_color=colors[idx],
            label=f"Community {idx+1}",
            node_size=500,
        )

    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

    plt.title("Network with Girvan-Newman Communities")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # edges_file = os.path.join(os.getcwd(), 'Cisco_22_networks/dir_20_graphs/dir_day1/out1_1.txt.gz')
    edges_file = os.path.join(
        os.getcwd(),
        "Cisco_22_networks/dir_g21_small_workload_with_gt/dir_no_packets_etc/edges_2days_feb10thruFeb11_all_49sensors.csv.txt.gz",
    )

    G = read_edges_with_ports_to_graph(edges_file)

    communities = run_girvan_newman(G)

    print(f"Detected communities: {communities}")

    draw_communities(G=G, communities=communities)


def run(path: str):
    edges_file = os.path.join(
        os.getcwd(),
        path,
    )

    G = read_edges_with_ports_to_graph(edges_file)

    communities = run_girvan_newman(G)

    return {"Detected communities": communities}
