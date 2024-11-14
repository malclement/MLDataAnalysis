import gzip
import io
from typing import Any

import networkx as nx


def read_edges_with_ports_to_graph(edges_file: str) -> nx.Graph:
    """
    Read a .txt.gz file containing edges with optional port information and create a NetworkX graph.
    """
    G = nx.Graph()

    with gzip.open(edges_file, mode="rt") as f:
        for line in f:
            if line.startswith("#"):
                continue

            parts = line.strip().split()

            if len(parts) < 2:
                continue

            source, target = parts[:2]

            if len(parts) >= 3:
                port = parts[2]
                G.add_edge(source, target, port=port)
            else:
                G.add_edge(source, target)

    return G


def save_plot(plot: Any) -> io.BytesIO:
    """
    Saves a Matplotlib plot to an in-memory BytesIO buffer as a PNG image.

    Args:
        plot (Any): The Matplotlib plot object (usually matplotlib.pyplot or a Figure object).

    Returns:
        io.BytesIO: A buffer containing the PNG image data of the plot.
    """
    buf = io.BytesIO()
    plot.savefig(buf, format="png")
    buf.seek(0)
    plot.close()
    return buf
