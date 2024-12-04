from collections import Counter
from typing import Dict
from typing import Set

import plotly.graph_objects as go
from fastapi import HTTPException
from fastapi import status


class GroundTruthStatistics:
    """
    Computes statistics from ground truth data.

    Attributes:
        num_groups (int): Number of groups.
        group_sizes (Dict[int, int]): Mapping from group ID to the size of the group.
        histogram (Counter): Histogram of group sizes.
    """

    def __init__(self, gt_to_nodes: Dict[int, Set[str]]):
        if not isinstance(gt_to_nodes, dict):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="gt_to_nodes must be a dictionary with group IDs as keys.",
            )
        if not all(isinstance(group_id, int) for group_id in gt_to_nodes.keys()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="All group IDs in gt_to_nodes must be integers.",
            )
        if not all(isinstance(nodes, set) for nodes in gt_to_nodes.values()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="All values in gt_to_nodes must be sets of node IDs.",
            )
        if not all(
            all(isinstance(node_id, str) for node_id in nodes)
            for nodes in gt_to_nodes.values()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="All node IDs in the sets must be strings.",
            )

        self.num_groups: int = 0
        self.group_sizes: Dict[int, int] = {}
        self.histogram: Counter = Counter()
        self._compute_statistics(gt_to_nodes)

    def _compute_statistics(self, gt_to_nodes: Dict[int, Set[str]]) -> None:
        """
        Computes statistics from gt_to_nodes mapping.
        """
        try:
            self.num_groups = len(gt_to_nodes)
            self.group_sizes = {
                group_id: len(nodes) for group_id, nodes in gt_to_nodes.items()
            }
            if not self.group_sizes:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No group sizes to compute; group_sizes is empty.",
                )
            self.histogram = Counter(self.group_sizes.values())
            if not self.histogram:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to compute histogram; it is empty.",
                )
        except HTTPException:
            # Re-raise HTTPExceptions to be handled by FastAPI
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error computing statistics: {str(exc)}",
            ) from exc

    def plot_group_size_histogram(
        self, title: str = "Histogram of Group Sizes"
    ) -> go.Figure:
        """
        Creates a histogram visualization of group sizes.

        Parameters:
            title (str): The title for the plot.

        Returns:
            go.Figure: A Plotly figure object representing the histogram.
        """
        if not self.histogram:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Histogram data is empty. Cannot plot histogram.",
            )

        group_sizes = list(self.histogram.keys())
        frequencies = list(self.histogram.values())

        if not group_sizes or not frequencies:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient data to generate histogram plot.",
            )

        try:
            fig = go.Figure(
                data=[
                    go.Bar(
                        x=group_sizes,
                        y=frequencies,
                        text=frequencies,
                        textposition="auto",
                    )
                ],
                layout=go.Layout(
                    title=title,
                    xaxis=dict(title="Group Size"),
                    yaxis=dict(title="Frequency"),
                    bargap=0.2,
                ),
            )
            return fig
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generating histogram plot: {str(exc)}",
            ) from exc
