from backend.tools.community_base import CommunityDetectionFactory
from backend.tools.custom_enums import CommunityAlgorithm
from backend.tools.custom_enums import FileSize
from backend.tools.path_selecter import path_selecter


def run_community_service(
    algorithm: CommunityAlgorithm, file_size: FileSize, viz: bool = False
):
    path = path_selecter(file_size=file_size)
    community_detector = CommunityDetectionFactory.get_community_detector(algorithm)

    if not viz:
        return community_detector.run(path)
    return community_detector.run_viz(path)
