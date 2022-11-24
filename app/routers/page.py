from typing import List, Optional

from fastapi import APIRouter, Depends, Form, Response, status
from fastapi.responses import JSONResponse

from app.auth.access import get_actual_user
from app.models.result import Result
from app.models.page import Page, PageInDB
from app.models.user import UserInDB
from app.services.page import PageService
from app.utils.mongo_validator import PyObjectId

router = APIRouter()


@router.get("", response_model=List[Page], status_code=status.HTTP_200_OK)
async def get_page(
    user: UserInDB = Depends(get_actual_user),
    q: Optional[str] = None,
    page_number: int = 0,
    n_per_page: int = 100,
):
    if q is not None:
        search = PageService.search(q=q, page_number=page_number, n_per_page=n_per_page)
    else:
        search = PageService.list(page_number=page_number, n_per_page=n_per_page)
    return search


@router.post(
    "",
    response_model=Page,
    status_code=status.HTTP_201_CREATED,
)
async def insert_page(
    title: str = Form(),
    slug: str = Form(),
    htmlarea: str = Form(
        default="""<!DOCTYPE html>\n<html>\n\t<body>\n\t</body>\n</html>"""
    ),
    user: UserInDB = Depends(get_actual_user),
):
    item = Page(title=title, slug=slug, html=htmlarea)
    item.id = None
    itemDB = PageInDB(**item.dict(by_alias=True))
    itemDB.username_insert = user.username
    inserted = PageService.insert(item=itemDB)
    return inserted


@router.put(
    "",
    responses={
        status.HTTP_200_OK: {"model": Page},
        status.HTTP_400_BAD_REQUEST: {"model": Result},
        status.HTTP_404_NOT_FOUND: {"model": Result},
    },
)
async def update_page(
    id: PyObjectId,
    title: str = Form(),
    slug: str = Form(),
    htmlarea: str = Form(
        default="""<!DOCTYPE html>\n<html>\n\t<body>\n\t</body>\n</html>"""
    ),
    user: UserInDB = Depends(get_actual_user),
):
    item = Page(_id=id, title=title, slug=slug, html=htmlarea)
    if item.id is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=Result(message="Id Field Not Found").dict(),
        )
    itemDB = PageInDB(**item.dict(by_alias=True))
    itemDB.username_update = user.username
    updated = PageService.update(itemDB)
    if updated is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=Result(message="Page Not Found").dict(),
        )
    else:
        return updated


@router.delete(
    "",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Result},
        status.HTTP_204_NO_CONTENT: {"model": None},
    },
)
async def delete_page(id: PyObjectId, user: UserInDB = Depends(get_actual_user)):
    itemDB = PageInDB(slug="", title="", html="")
    itemDB.id = id
    itemDB.username_update = user.username
    deleted = PageService.delete(item=itemDB)
    if deleted is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=Result(message="Page Not Found").dict(),
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
