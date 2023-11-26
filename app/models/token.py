from datetime import datetime
from typing import Optional


from pydantic import BaseModel
from pydantic.fields import Field

from app.utils import PyObjectId


class Token(BaseModel):
    """Model for TOKEN in database, used in API operations, require email and token"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: str
    token: str
    username: Optional[str] = ""
    disabled: Optional[bool] = False
    date_insert: Optional[datetime] = None
    date_update: Optional[datetime] = None
    username_insert: Optional[str] = None
    username_update: Optional[str] = None
