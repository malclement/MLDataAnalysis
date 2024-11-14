import os
from enum import Enum

from community_detection.girvan_newman import run as run_girvan_newman
from community_detection.label_propagation import run as run_label_propagation
from community_detection.louvain import run as run_louvain

small_path = "Cisco_22_networks/dir_g21_small_workload_with_gt/dir_no_packets_etc/edges_2days_feb10thruFeb11_all_49sensors.csv.txt.gz"
large_path = "Cisco_22_networks/dir_20_graphs/dir_day1/out1_1.txt.gz"


class CommunityAlgorithm(str, Enum):
    GIRVAN_NEWMAN = "Girvan-Newman"
    LOUVAIN = "Louvain"
    LABEL_PROPAGATION = "Label Propagation"


class FileSize(str, Enum):
    LARGE = "Large"
    SMALL = "Small"


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
