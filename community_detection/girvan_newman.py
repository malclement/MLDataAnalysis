import os
import networkx as nx
from networkx.algorithms.community import girvan_newman
import gzip

def read_edges_with_ports_to_graph(edges_file):
    G = nx.Graph()
    with gzip.open(edges_file, mode='rt') as fopen:
        for line in fopen:
            if line.startswith('#'):  # skip comment lines
                continue
            parts = line.split()
            if len(parts) < 3:
                continue
            node1, node2 = parts[1], parts[2]
            G.add_edge(node1, node2)
    return G

def run_girvan_newman(G):
    comp = girvan_newman(G)
    communities = tuple(sorted(c) for c in next(comp))
    return communities

if __name__ == '__main__':
    # Replace with the path to your edge file
    # edges_file = os.path.join(os.getcwd(), 'Cisco_22_networks/dir_20_graphs/dir_day1/out1_1.txt.gz')
    edges_file = os.path.join(os.getcwd(), 'Cisco_22_networks/dir_g21_small_workload_with_gt/dir_no_packets_etc/edges_2days_feb10thruFeb11_all_49sensors.csv.txt.gz')

    # Read edges and build the graph
    G = read_edges_with_ports_to_graph(edges_file)
    
    # Run Girvan-Newman Algorithm
    communities = run_girvan_newman(G)
    
    # Output the detected communities
    print(f"Detected communities: {communities}")
