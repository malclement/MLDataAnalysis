from fastapi import FastAPI
from fastapi import Query
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates

from backend.services.community_services import run_community_service
from backend.services.gt_services import display_histogram_service
from backend.services.gt_services import ground_truth_service
from backend.services.gt_services import ground_truth_statistics_service
from backend.services.gt_services import ground_truth_visualization_service
from backend.tools.custom_enums import CommunityAlgorithm
from backend.tools.custom_enums import FileSize

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse, tags=["Base"])
async def root(request: Request):
    return templates.TemplateResponse("homepage.html", context={"request": request})


@app.get("/health", response_class=JSONResponse, tags=["Base"])
async def health_check():
    return {"status": "healthy"}


@app.get("/community/{algorithm}", response_class=JSONResponse, tags=["Community"])
async def run_community(
    algorithm: CommunityAlgorithm, file_size: FileSize = FileSize.SMALL
):
    return run_community_service(algorithm=algorithm, file_size=file_size)


@app.get("/gd", response_class=JSONResponse, tags=["Ground Truth"])
async def ground_truth(file_size: FileSize = FileSize.SMALL):
    return ground_truth_service(file_size=file_size)


@app.get("/gd/visualize", response_class=HTMLResponse, tags=["Ground Truth"])
async def ground_truth_visualization(
    file_size: FileSize = FileSize.SMALL,
    save: bool = Query(False, description="Save as img"),
):
    return ground_truth_visualization_service(file_size=file_size)


@app.get("/gd/stats", response_class=JSONResponse, tags=["Ground Truth"])
async def ground_truth_statistics(file_size: FileSize = FileSize.SMALL):
    return ground_truth_statistics_service(file_size=file_size)


@app.get("/gd/histogram", response_class=HTMLResponse, tags=["Ground Truth"])
async def ground_truth_histogram(file_size: FileSize = FileSize.SMALL):
    return display_histogram_service(file_size=file_size)
