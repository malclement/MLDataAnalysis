from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates
from magnum import Mangum

from backend.routes.community_routes import community_router
from backend.routes.gt_routes import gt_router

app = FastAPI(
    title="Cisco Analysis - API",
    description="API to trigger cisco analysis mechanism",
    version="1.0.0",
    redoc_url="/docs",
)

templates = Jinja2Templates(directory="templates")

app.include_router(router=gt_router)
app.include_router(router=community_router)


@app.get("/", response_class=HTMLResponse, tags=["Base"])
async def root(request: Request):
    return templates.TemplateResponse("homepage.html", context={"request": request})


@app.get("/health", response_class=JSONResponse, tags=["Base"])
async def health_check():
    return {"status": "healthy"}


handler = Mangum(app)