import json

from fastapi import Request, Security, status
from fastapi.exceptions import HTTPException
from fastapi.security.api_key import APIKeyHeader
from jose import jws

from app.core import configuration
from app.models.token import Token
from app.models.user import UserInDB
from app.services.token import TokenService
from app.services.user import UserService


async def get_actual_user(request: Request) -> UserInDB | None:
    user = request.session.get("user")
    if user is not None:
        userDB = UserService.get_user(UserInDB(username=user["email"]))
        if userDB is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User not Found"
            )
        if userDB.disabled == True:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User Disabled"
            )
        if userDB.admin == False:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="You are not admin"
            )
        return userDB
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials.",
        )


SECRET = configuration.APP_SECRET_TOKENS
api_key_header = APIKeyHeader(name="Authorization", auto_error=True)


async def get_api_key(api_key: str = Security(api_key_header)):
    api_key = api_key.replace("Bearer ", "", 1)
    token = Token(token=api_key, username="")
    ret = TokenService.get_token(token)
    if ret is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Token unvalid"
        )
    else:
        try:
            user = jws.verify(api_key, SECRET, algorithms=[configuration.APP_TOKEN_ALGORITHM])
            return UserInDB(**dict(json.loads(user)))
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Token unvalid"
            )
