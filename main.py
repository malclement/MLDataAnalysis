from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates

from backend.routes.gt_routes import gt_router
from backend.services.community_services import run_community_service
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
