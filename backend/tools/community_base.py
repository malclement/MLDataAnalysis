from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import networkx as nx
from sklearn.cluster import SpectralClustering

from backend.tools.custom_enums import CommunityAlgorithm
from backend.tools.graph_utils import create_html_visualization
from backend.tools.graph_utils import read_edges_with_ports_to_graph


class CommunityDetectionBase(ABC):
    """
    Abstract base class for community detection algorithms.
    """

    @abstractmethod
    def detect_communities(
        self, G: nx.Graph
    ) -> Union[Dict[str, int], Tuple[List[str], ...]]:
        """
        Abstract method to be implemented by specific algorithms for community detection.
        """
        pass

    def run(self, path: str) -> Union[Dict[str, int], Tuple[List[str], ...]]:
        """
        Run the community detection algorithm on a graph built from the file.
        """
        G = read_edges_with_ports_to_graph(path)
        return self.detect_communities(G)

    def run_viz(self, path: str) -> str:
        """
        Run the community detection algorithm and create an HTML visualization.
        """
        G = read_edges_with_ports_to_graph(path)
        communities = self.detect_communities(G)
        return create_html_visualization(G, communities)


class LabelPropagation(CommunityDetectionBase):
    def detect_communities(self, G: nx.Graph) -> Dict[str, int]:
        communities = nx.community.label_propagation_communities(G)
        return {
            node: i for i, community in enumerate(communities) for node in community
        }


class Louvain(CommunityDetectionBase):
    def detect_communities(self, G: nx.Graph) -> Dict[str, int]:
        partition = nx.community.louvain_communities(G)
        return {node: i for i, community in enumerate(partition) for node in community}


class GirvanNewman(CommunityDetectionBase):
    def detect_communities(self, G: nx.Graph) -> Tuple[List[str], ...]:
        comp = nx.community.girvan_newman(G)
        return tuple(sorted(c) for c in next(comp))


class SpectralClusteringAlgorithm(CommunityDetectionBase):
    def detect_communities(self, G: nx.Graph) -> Dict[str, int]:
        """
        Detect communities using spectral clustering.
        """
        adjacency_matrix = nx.to_numpy_array(G)
        clustering = SpectralClustering(
            n_clusters=min(10, len(G.nodes)), affinity="precomputed", random_state=42
        ).fit(adjacency_matrix)
        return {
            str(node): int(label) for node, label in zip(G.nodes(), clustering.labels_)
        }


class ModularityMaximization(CommunityDetectionBase):
    def detect_communities(self, G: nx.Graph) -> Dict[str, int]:
        return nx.community.greedy_modularity_communities(G)


class KernighanLinAlgorithm(CommunityDetectionBase):
    def detect_communities(self, G: nx.Graph) -> Dict[str, int]:
        partition = nx.algorithms.community.kernighan_lin_bisection(G)
        return {node: idx for idx, group in enumerate(partition) for node in group}


class CommunityDetectionFactory:
    """
    Factory class to create instances of community detection algorithms.
    """

    @staticmethod
    def get_community_detector(algorithm: CommunityAlgorithm) -> CommunityDetectionBase:
        if algorithm == CommunityAlgorithm.LOUVAIN:
            return Louvain()
        elif algorithm == CommunityAlgorithm.LABEL_PROPAGATION:
            return LabelPropagation()
        elif algorithm == CommunityAlgorithm.GIRVAN_NEWMAN:
            return GirvanNewman()
        elif algorithm == CommunityAlgorithm.SPECTRAL:
            return SpectralClusteringAlgorithm()
        elif algorithm == CommunityAlgorithm.MODULARITY:
            return ModularityMaximization()
        elif algorithm == CommunityAlgorithm.KERNIGHAN_LIN:
            return KernighanLinAlgorithm()
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
