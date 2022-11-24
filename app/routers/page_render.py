
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.models.result import Result
from app.services.page import PageService
from fastapi.responses import HTMLResponse
router = APIRouter()


@router.get("/{slug}")
async def get_page(slug: str):
    search = PageService.get_by_slug(slug=slug)
    if search is not None:
        return HTMLResponse(content=search.html, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=Result(message="Page not Found").dict(),
        )