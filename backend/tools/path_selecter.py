from backend.tools.custom_enums import FileSize

small_path = "Cisco_22_networks/dir_g21_small_workload_with_gt/dir_no_packets_etc/edges_2days_feb10thruFeb11_all_49sensors.csv.txt.gz"
large_path = "Cisco_22_networks/dir_20_graphs/dir_day1/out1_1.txt.gz"
test = "Cisco_22_networks/dir_g21_small_workload_with_gt/grouping.gt.txt"


def path_selecter(file_size: FileSize) -> str:
    if file_size == FileSize.LARGE:
        return large_path
    return small_path
