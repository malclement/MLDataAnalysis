import os
import random
from typing import List
from typing import Tuple

import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms.community import girvan_newman

from community_detection import read_edges_with_ports_to_graph


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
