import os

from community_detection.girvan_newman import run as run_girvan_newman

path = "Cisco_22_networks/dir_g21_small_workload_with_gt/dir_no_packets_etc/edges_2days_feb10thruFeb11_all_49sensors.csv.txt.gz"


def run_community_service():
    return run_girvan_newman(path)
