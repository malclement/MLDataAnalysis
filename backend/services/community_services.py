import gzip
from collections import defaultdict

from backend.services.custom_enums import CommunityAlgorithm
from backend.services.custom_enums import FileSize
from community_detection.girvan_newman import run as run_girvan_newman
from community_detection.label_propagation import run as run_label_propagation
from community_detection.louvain import run as run_louvain

small_path = "Cisco_22_networks/dir_g21_small_workload_with_gt/dir_no_packets_etc/edges_2days_feb10thruFeb11_all_49sensors.csv.txt.gz"
large_path = "Cisco_22_networks/dir_20_graphs/dir_day1/out1_1.txt.gz"


def path_selecter(file_size: FileSize) -> str:
    if file_size == FileSize.LARGE:
        return large_path
    return small_path


def run_community_service(algorithm: CommunityAlgorithm, file_size: FileSize):
    path = path_selecter(file_size=file_size)

    if algorithm == CommunityAlgorithm.LOUVAIN:
        return run_louvain(path=path)
    if algorithm == CommunityAlgorithm.LABEL_PROPAGATION:
        return run_label_propagation(path=path)
    return run_girvan_newman(path=path)


def get_ground_truth(file_size: FileSize):
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
