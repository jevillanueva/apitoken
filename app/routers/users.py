from typing import Optional

from fastapi import APIRouter, Depends

from app.auth.access import get_actual_user
from app.models.user import User

router = APIRouter()


@router.get("/me", response_model=User)
async def get_me(user: Optional[dict] = Depends(get_actual_user)):
    return user
