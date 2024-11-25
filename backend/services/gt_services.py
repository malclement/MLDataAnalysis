import gzip
import os
from collections import defaultdict

import networkx as nx
import plotly.graph_objects as go
import plotly.io as pio
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse

from backend.tools.custom_enums import FileSize
from backend.tools.path_selecter import path_selecter


def ground_truth_service(file_size: FileSize):
    """
    This function reads a ground truth file (including gzipped files) and returns two mappings:
    1. node_gt: A dictionary mapping node ID to group ID.
    2. gt_to_nodes: A dictionary mapping group ID to a set of nodes in that group.

    Parameters:
    - gt_file: Path to the ground truth file.

    Returns:
    - node_gt: Dictionary mapping node to group ID.
    - gt_to_nodes: Dictionary mapping group ID to set of nodes.
    """
    gt_file = path_selecter(file_size=file_size)
    node_gt = {}
    gt_to_nodes = defaultdict(set)

    if gt_file.endswith(".gz"):
        with gzip.open(gt_file, "rt", encoding="utf-8") as f:
            group_id = 0

            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                group_id += 1
                parts = line.split(",")

                for node_id in parts:
                    node_gt[node_id] = group_id
                    gt_to_nodes[group_id].add(node_id)
    else:
        with open(gt_file, "r", encoding="utf-8") as f:
            group_id = 0
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                group_id += 1
                parts = line.split(",")

                for node_id in parts:
                    node_gt[node_id] = group_id
                    gt_to_nodes[group_id].add(node_id)

    return node_gt, gt_to_nodes
