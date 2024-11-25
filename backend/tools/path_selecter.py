from backend.tools.custom_enums import FileSize

small_2d_path = "Cisco_22_networks/dir_g21_small_workload_with_gt/dir_no_packets_etc/edges_2days_feb10thruFeb11_all_49sensors.csv.txt.gz"
small_4d_path = "Cisco_22_networks/dir_g21_small_workload_with_gt/dir_no_packets_etc/edges_4days_feb10thruFeb13_all_49sensors.csv.txt.gz"
small_12h_path = "Cisco_22_networks/dir_g21_small_workload_with_gt/dir_no_packets_etc/edges_12hrs_feb10_all_49sensors.csv.txt.gz"
large_path = "Cisco_22_networks/dir_20_graphs/dir_day1/out1_1.txt.gz"
test = "Cisco_22_networks/dir_g21_small_workload_with_gt/grouping.gt.txt"


rnd_small = [
    "Cisco_22_networks/dir_g21_small_workload_with_gt/dir_no_packets_etc/edges_2days_feb10thruFeb11_all_49sensors.csv.txt.gz",
    "Cisco_22_networks/dir_g21_small_workload_with_gt/dir_no_packets_etc/edges_4days_feb10thruFeb13_all_49sensors.csv.txt.gz",
    "Cisco_22_networks/dir_g21_small_workload_with_gt/dir_no_packets_etc/edges_12hrs_feb10_all_49sensors.csv.txt.gz",
]


def path_selecter(file_size: FileSize) -> str:
    if file_size == FileSize.LARGE:
        return large_path
    if file_size == FileSize.SMALL_12H:
        return small_12h_path
    if file_size == FileSize.SMALL_2D:
        return small_2d_path
    if file_size == FileSize.SMALL_4D:
        return small_4d_path
    if file_size == FileSize.TEST:
        return test
    return small_2d_path
