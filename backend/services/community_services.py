from backend.tools.custom_enums import CommunityAlgorithm
from backend.tools.custom_enums import FileSize
from backend.tools.path_selecter import path_selecter
from community_detection.girvan_newman import run as run_girvan_newman
from community_detection.label_propagation import run as run_label_propagation
from community_detection.louvain import run as run_louvain


def run_community_service(algorithm: CommunityAlgorithm, file_size: FileSize):
    path = path_selecter(file_size=file_size)

    if algorithm == CommunityAlgorithm.LOUVAIN:
        return run_louvain(path=path)
    if algorithm == CommunityAlgorithm.LABEL_PROPAGATION:
        return run_label_propagation(path=path)
    return run_girvan_newman(path=path)
