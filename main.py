from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates

from backend.services.community_services import get_ground_truth
from backend.services.community_services import run_community_service
from backend.services.custom_enums import CommunityAlgorithm
from backend.services.custom_enums import FileSize

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
    return get_ground_truth(file_size=file_size)
