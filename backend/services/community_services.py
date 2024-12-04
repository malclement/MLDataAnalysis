from backend.tools.custom_enums import CommunityAlgorithm
from backend.tools.custom_enums import FileSize
from backend.tools.path_selecter import path_selecter
from community_detection.girvan_newman import run as run_girvan_newman
from community_detection.girvan_newman import run_viz as viz_girvan_newman
from community_detection.label_propagation import run as run_label_propagation
from community_detection.label_propagation import run_viz as viz_label_propagation
from community_detection.louvain import run as run_louvain
from community_detection.louvain import run_viz as viz_louvain


def run_community_service(
    algorithm: CommunityAlgorithm, file_size: FileSize, viz: bool = False
):
    path = path_selecter(file_size=file_size)

    if not viz:
        if algorithm == CommunityAlgorithm.LOUVAIN:
            return run_louvain(path=path)
        if algorithm == CommunityAlgorithm.LABEL_PROPAGATION:
            return run_label_propagation(path=path)
        return run_girvan_newman(path=path)

    else:
        if algorithm == CommunityAlgorithm.LOUVAIN:
            return viz_louvain(path=path)
        if algorithm == CommunityAlgorithm.GIRVAN_NEWMAN:
            return viz_girvan_newman(path=path)
        if algorithm == CommunityAlgorithm.LABEL_PROPAGATION:
            return viz_label_propagation(path=path)
    return
