from backend.tools.community_base import CommunityDetectionFactory
from backend.tools.custom_enums import CommunityAlgorithm
from backend.tools.custom_enums import FileSize
from backend.tools.path_selecter import path_selecter


def run_community_service(
    algorithm: CommunityAlgorithm, file_size: FileSize, viz: bool = False
):
    # Select the path based on file size
    path = path_selecter(file_size=file_size)

    # Get the appropriate community detection instance
    community_detector = CommunityDetectionFactory.get_community_detector(algorithm)

    if not viz:
        # Run the detection algorithm
        return community_detector.run(path)
    else:
        # Run the visualization
        return community_detector.run_viz(path)
