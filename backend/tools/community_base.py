from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

import networkx as nx

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
        """
        Detect communities using the Label Propagation algorithm.
        """
        communities = nx.community.label_propagation_communities(G)
        partition = {}
        for i, community in enumerate(communities):
            for node in community:
                partition[node] = i
        return partition


class Louvain(CommunityDetectionBase):
    def detect_communities(self, G: nx.Graph) -> Dict[str, int]:
        """
        Detect communities using the Louvain algorithm.
        """
        partition = nx.community.louvain_communities(G)
        node_community_map = {}
        for community_id, nodes in enumerate(partition):
            for node in nodes:
                node_community_map[node] = community_id
        return node_community_map


class GirvanNewman(CommunityDetectionBase):
    def detect_communities(self, G: nx.Graph) -> Tuple[List[str], ...]:
        """
        Detect communities using the Girvan-Newman algorithm.
        """
        comp = nx.community.girvan_newman(G)
        return tuple(sorted(c) for c in next(comp))


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
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
