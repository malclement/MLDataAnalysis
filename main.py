from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates

from backend.services.community_services import CommunityAlgorithm
from backend.services.community_services import run_community_service

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse, tags=["Base"])
async def root(request: Request):
    return templates.TemplateResponse("homepage.html", context={"request": request})


@app.get("/health", response_class=JSONResponse, tags=["Base"])
async def health_check():
    return {"status": "healthy"}


@app.get("/community/{algorithm}", response_class=JSONResponse, tags=["Community"])
async def run_community(algorithm: CommunityAlgorithm):
    return run_community_service(algorithm=algorithm)
