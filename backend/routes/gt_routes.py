from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse

from backend.services.gt_services import GroundTruth
from backend.services.gt_statistic_services import GroundTruthStatistics
from backend.tools.custom_enums import FileSize

gt_router = APIRouter(prefix="/gt", tags=["Ground Truth"])


@gt_router.get("/", response_class=JSONResponse)
async def ground_truth(file_size: FileSize = FileSize.SMALL_2D):
    gt = GroundTruth(file_size=file_size)
    return {"node_gt": gt.node_gt, "gt_to_nodes": gt.gt_to_nodes}


@gt_router.get("/stats", response_class=JSONResponse)
async def ground_truth_statistics(file_size: FileSize = FileSize.SMALL_2D):
    gt = GroundTruth(file_size=file_size)
    stats = GroundTruthStatistics(gt.gt_to_nodes)
    return {
        "num_groups": stats.num_groups,
        "group_sizes": stats.group_sizes,
        "histogram": dict(stats.histogram),
    }


@gt_router.get("/histogram", response_class=HTMLResponse)
async def ground_truth_histogram(file_size: FileSize = FileSize.SMALL_2D):
    gt = GroundTruth(file_size=file_size)
    stats = GroundTruthStatistics(gt.gt_to_nodes)
    fig = stats.plot_group_size_histogram()
    return HTMLResponse(content=fig.to_html(full_html=False), status_code=200)
