import gzip
from collections import defaultdict
from typing import Dict
from typing import Set

from backend.tools.custom_enums import FileSize
from backend.tools.path_selecter import path_selecter


class GroundTruth:
    """
    Represents ground truth data, providing mappings between nodes and groups.

    Attributes:
        node_gt (Dict[str, int]): Mapping from node ID to group ID.
        gt_to_nodes (Dict[int, Set[str]]): Mapping from group ID to set of node IDs.
        file_size (FileSize): The size category of the file to be processed.
    """

    def __init__(self, file_size: FileSize):
        self.node_gt: Dict[str, int] = {}
        self.gt_to_nodes: Dict[int, Set[str]] = defaultdict(set)
        self.file_size: FileSize = file_size
        self._load_data()

    def _load_data(self) -> None:
        """
        Loads ground truth data from a file into node_gt and gt_to_nodes mappings.
        """
        gt_file = path_selecter(file_size=self.file_size)
        group_id = 0

        open_func = gzip.open if gt_file.endswith(".gz") else open
        with open_func(gt_file, "rt", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                group_id += 1
                parts = line.split(",")
                for node_id in parts:
                    self.node_gt[node_id] = group_id
                    self.gt_to_nodes[group_id].add(node_id)
