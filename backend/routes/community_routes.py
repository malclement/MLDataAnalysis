from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse

from backend.services.community_services import run_community_service
from backend.tools.custom_enums import CommunityAlgorithm
from backend.tools.custom_enums import FileSize


community_router = APIRouter(prefix="/community", tags=["Community"])


@community_router.get("/{algorithm}", response_class=JSONResponse, tags=["Community"])
async def run_community(
    algorithm: CommunityAlgorithm, file_size: FileSize = FileSize.SMALL_2D
):
    return run_community_service(algorithm=algorithm, file_size=file_size)


@community_router.get(
    "/{algorithm}/viz", response_class=HTMLResponse, tags=["Community"]
)
async def viz_community(
    algorithm: CommunityAlgorithm, file_size: FileSize = FileSize.SMALL_2D
):
    return run_community_service(algorithm=algorithm, file_size=file_size, viz=True)
