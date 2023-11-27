from datetime import datetime
from typing import Optional


from pydantic import BaseModel
from pydantic.fields import Field

from app.utils import PyObjectId


class Token(BaseModel):
    """Model for TOKEN in database, used in API operations, require email and token"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: str
    jti: str
    disabled: Optional[bool] = False
    date_insert: Optional[datetime] = None
    date_update: Optional[datetime] = None
    username_insert: Optional[str] = None
    username_update: Optional[str] = None

class TokenUser(BaseModel):
    """Model for Token to send to user"""
    token: str
    jti: str