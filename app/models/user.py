from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from app.utils.mongo_validator import PyObjectId


class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str
    email: Optional[str] = None
    picture: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    disabled: Optional[bool] = False
    admin: Optional[bool] = False


class UserInDB(User):
    hashed_password: Optional[str] = None
    date_insert: Optional[datetime] = None
    date_update: Optional[datetime] = None
