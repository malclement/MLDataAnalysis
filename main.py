from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates

from backend.routes.gt_routes import gt_router
from backend.services.community_services import run_community_service
from backend.services.network_vizualisation_services import visualization_service
from backend.tools.custom_enums import CommunityAlgorithm
from backend.tools.custom_enums import FileSize

app = FastAPI(
    title="Cisco Analysis - API",
    description="API to trigger cisco analysis mechanism",
    version="1.0.0",
    redoc_url="/docs",
)

templates = Jinja2Templates(directory="templates")

app.include_router(gt_router)


@app.get("/", response_class=HTMLResponse, tags=["Base"])
async def root(request: Request):
    return templates.TemplateResponse("homepage.html", context={"request": request})


@app.get("/health", response_class=JSONResponse, tags=["Base"])
async def health_check():
    return {"status": "healthy"}


@app.get("/community/{algorithm}", response_class=JSONResponse, tags=["Community"])
async def run_community(
    algorithm: CommunityAlgorithm, file_size: FileSize = FileSize.SMALL_2D
):
    return run_community_service(algorithm=algorithm, file_size=file_size)


@app.get("/community/{algorithm}/viz", response_class=HTMLResponse, tags=["Community"])
async def viz_community(
    algorithm: CommunityAlgorithm, file_size: FileSize = FileSize.SMALL_2D
):
    return run_community_service(algorithm=algorithm, file_size=file_size, viz=True)


@app.get("/viz", response_class=HTMLResponse)
async def visualization(file_size: FileSize = FileSize.SMALL_2D):
    return visualization_service(file_size=file_size)
