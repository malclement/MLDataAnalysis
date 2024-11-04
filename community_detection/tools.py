import gzip
import io
from typing import Any

import networkx as nx


def read_edges_with_ports_to_graph(edges_file: str) -> nx.Graph:
    graph = nx.Graph()
    with gzip.open(edges_file, mode="rt") as fopen:
        for line in fopen:
            if line.startswith("#"):  # skip comment lines
                continue
            parts = line.split()
            if len(parts) < 3:
                continue
            node1, node2 = parts[1], parts[2]
            graph.add_edge(node1, node2)
    return graph


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
