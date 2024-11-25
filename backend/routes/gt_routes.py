from fastapi import APIRouter
from fastapi import Query
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse

from backend.services.gt_services import ground_truth_service
from backend.services.gt_services import ground_truth_visualization_service
from backend.services.gt_statistic_services import display_histogram_service
from backend.services.gt_statistic_services import ground_truth_statistics_service
from backend.tools.custom_enums import FileSize

gt_router = APIRouter(prefix="/gt", tags=["Ground Truth"])


@gt_router.get("/", response_class=JSONResponse)
async def ground_truth(file_size: FileSize = FileSize.SMALL):
    return ground_truth_service(file_size=file_size)


@gt_router.get("/vizualise", response_class=HTMLResponse)
async def ground_truth_visualization(
    file_size: FileSize = FileSize.SMALL,
    save: bool = Query(False, description="Save as img"),
):
    return ground_truth_visualization_service(file_size=file_size)


@gt_router.get("/stats", response_class=JSONResponse)
async def ground_truth_statistics(file_size: FileSize = FileSize.SMALL):
    return ground_truth_statistics_service(file_size=file_size)


@gt_router.get("/histogram", response_class=HTMLResponse)
async def ground_truth_histogram(file_size: FileSize = FileSize.SMALL):
    return display_histogram_service(file_size=file_size)
