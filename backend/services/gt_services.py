import gzip
from collections import defaultdict
from typing import Dict
from typing import Set

from fastapi import HTTPException
from fastapi import status

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

        try:
            with open_func(gt_file, "rt", encoding="utf-8") as f:
                for line_number, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    group_id += 1
                    parts = line.split(",")
                    if not parts:
                        raise ValueError(f"Invalid data format in line {line_number}.")
                    for node_id in parts:
                        node_id = node_id.strip()
                        if not node_id:
                            raise ValueError(
                                f"Empty node ID found in line {line_number}."
                            )
                        self.node_gt[node_id] = group_id
                        self.gt_to_nodes[group_id].add(node_id)

            if not self.node_gt:
                raise ValueError("No ground truth data found in the file.")

        except FileNotFoundError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ground truth file not found: {gt_file}",
            ) from exc
        except gzip.BadGzipFile as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid gzip file: {gt_file}",
            ) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while loading ground truth data: {str(exc)}",
            ) from exc
