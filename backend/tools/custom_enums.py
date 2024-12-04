from enum import Enum


class CommunityAlgorithm(str, Enum):
    GIRVAN_NEWMAN = "Girvan-Newman"
    LOUVAIN = "Louvain"
    LABEL_PROPAGATION = "Label Propagation"
    SPECTRAL = "Spectral Clustering"
    MODULARITY = "Modularity Maximization"
    KERNIGHAN_LIN = "Kernighan-Lin"


class FileSize(str, Enum):
    LARGE = "Large"
    SMALL_2D = "Small 2 days"
    SMALL_4D = "Small 4 days"
    SMALL_12H = "Small 12 hours"
    TEST = "Test"
