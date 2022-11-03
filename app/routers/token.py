from typing import List, Optional

from fastapi import APIRouter, Depends, status
from starlette.responses import Response

from app.auth.access import get_actual_user, get_api_key
from app.models.result import Result
from app.models.token import Token
from app.models.user import UserInDB
from app.services.token import TokenService
from app.utils.mongo_validator import PyObjectId

router = APIRouter()


@router.get("", response_model=List[Token], status_code=status.HTTP_200_OK)
async def get_token(user: UserInDB = Depends(get_actual_user), q: Optional[str] = None):
    search = Token(token="", username=user.username)
    if q is not None:
        search.token = q
        tokens = TokenService.search(item=search)
    else:
        tokens = TokenService.get(search.username)
    return tokens


@router.post("", response_model=Token, status_code=status.HTTP_201_CREATED)
async def post_token(user: UserInDB = Depends(get_actual_user)):
    item = Token(token="", username=user.username)
    print(item)
    item.username_insert = user.username
    ret = TokenService.create(item)
    item.id = ret.inserted_id
    ret = TokenService.get_by_id_and_user(item)
    return ret


@router.delete(
    "",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": Result},
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_400_BAD_REQUEST: {"model": Result},
    },
)
async def delete_token(id: PyObjectId, user: UserInDB = Depends(get_actual_user)):
    item = Token(token="", username=user.username)
    item.id = id
    if item.id is None:
        return Result(code=0, message="ID token not Found"), status.HTTP_404_NOT_FOUND

    ret = TokenService.get_by_id_and_user(item)
    if ret is None:
        return Result(code=0, message="Token not Found"), status.HTTP_404_NOT_FOUND

    item.username_update = user.username
    ret = TokenService.delete(item)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/echo", response_model=str, status_code=status.HTTP_200_OK)
async def echo_test_token(
    q: Optional[str] = None,
    user: UserInDB = Depends(get_api_key)
):
    return f"{user.username} says: '{q}'"