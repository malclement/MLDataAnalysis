from enum import Enum


class CommunityAlgorithm(str, Enum):
    GIRVAN_NEWMAN = "Girvan-Newman"
    LOUVAIN = "Louvain"
    LABEL_PROPAGATION = "Label Propagation"


class FileSize(str, Enum):
    LARGE = "Large"
    SMALL_2D = "Small 2 days"
    SMALL_4D = "Small 4 days"
    SMALL_12H = "Small 12 hours"
    TEST = "Test"
