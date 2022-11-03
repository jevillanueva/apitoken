from datetime import datetime
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel
from pydantic.fields import Field

from app.utils.mongo_validator import PyObjectId


class Token(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str
    token: str
    disabled: Optional[bool] = False
    date_insert: Optional[datetime] = None
    date_update: Optional[datetime] = None
    username_insert: Optional[str] = None
    username_update: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
