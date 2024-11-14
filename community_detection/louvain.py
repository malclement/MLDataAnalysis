import os
import random
from typing import Dict

import matplotlib.pyplot as plt
import networkx as nx

from community_detection import read_edges_with_ports_to_graph


def run_louvain(G: nx.Graph) -> Dict[str, int]:
    # Using Louvain algorithm to partition the graph into communities
    partition = nx.community.louvain_communities(G)
    return partition


def draw_communities(G: nx.Graph, partition: Dict[str, int]):
    pos = nx.spring_layout(G)  # Positioning for nodes

    # Unique communities
    unique_communities = set(partition.values())
    colors = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in unique_communities]
    color_map = {
        community: colors[idx] for idx, community in enumerate(unique_communities)
    }

    plt.figure(figsize=(10, 10))

    # Drawing nodes with colors based on their community
    for node, community in partition.items():
        nx.draw_networkx_nodes(
            G,
            pos,
            nodelist=[node],
            node_color=color_map[community],
            node_size=500,
            label=f"Community {community}",
        )

    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="black")

    plt.title("Network with Louvain Communities")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    # Specify the edges file location
    edges_file = os.path.join(
        os.getcwd(),
        "Cisco_22_networks/dir_g21_small_workload_with_gt/dir_no_packets_etc/edges_2days_feb10thruFeb11_all_49sensors.csv.txt.gz",
    )

    G = read_edges_with_ports_to_graph(edges_file)

    partition = run_louvain(G)
    print(f"Detected communities: {partition}")

    draw_communities(G=G, partition=partition)


def run(path: str):
    edges_file = os.path.join(
        os.getcwd(),
        path,
    )

    G = read_edges_with_ports_to_graph(edges_file=edges_file)

    communities = run_louvain(G)

    return {"Detected communities": communities}
