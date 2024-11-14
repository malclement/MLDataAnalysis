from enum import Enum


class CommunityAlgorithm(str, Enum):
    GIRVAN_NEWMAN = "Girvan-Newman"
    LOUVAIN = "Louvain"
    LABEL_PROPAGATION = "Label Propagation"


class FileSize(str, Enum):
    LARGE = "Large"
    SMALL = "Small"
