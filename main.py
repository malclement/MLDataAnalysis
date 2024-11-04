from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("homepage.html", context={"request": request})


@app.get("/health", response_class=JSONResponse)
async def health_check():
    return {"status": "healthy"}


@app.get("/community", response_class=JSONResponse)
async def run_community():
    return {"status": "completed"}
