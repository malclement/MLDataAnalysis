import os
from enum import Enum

from community_detection.girvan_newman import run as run_girvan_newman

path = "Cisco_22_networks/dir_g21_small_workload_with_gt/dir_no_packets_etc/edges_2days_feb10thruFeb11_all_49sensors.csv.txt.gz"


class CommunityAlgorithm(str, Enum):
    GIRVAN_NEWMAN = "Girvan-Newman"
    LOUVAIN = "Louvain"


def run_community_service(algorithm: CommunityAlgorithm):
    if algorithm == CommunityAlgorithm.LOUVAIN:
        return
    return run_girvan_newman(path=path)
