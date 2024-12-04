from collections import Counter
from typing import Dict
from typing import Set

import plotly.graph_objects as go


class GroundTruthStatistics:
    """
    Computes statistics from ground truth data.

    Attributes:
        num_groups (int): Number of groups.
        group_sizes (Dict[int, int]): Mapping from group ID to the size of the group.
        histogram (Counter): Histogram of group sizes.
    """

    def __init__(self, gt_to_nodes: Dict[int, Set[str]]):
        self.num_groups: int = 0
        self.group_sizes: Dict[int, int] = {}
        self.histogram: Counter = Counter()
        self._compute_statistics(gt_to_nodes)

    def _compute_statistics(self, gt_to_nodes: Dict[int, Set[str]]) -> None:
        """
        Computes statistics from gt_to_nodes mapping.
        """
        self.num_groups = len(gt_to_nodes)
        self.group_sizes = {
            group_id: len(nodes) for group_id, nodes in gt_to_nodes.items()
        }
        self.histogram = Counter(self.group_sizes.values())

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
        group_sizes = list(self.histogram.keys())
        frequencies = list(self.histogram.values())

        fig = go.Figure(
            data=[
                go.Bar(
                    x=group_sizes, y=frequencies, text=frequencies, textposition="auto"
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
