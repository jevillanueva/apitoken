from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.utils import PyObjectId


class Page(BaseModel):
    """Model for Page, used for return HTML page require slug and title"""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    slug: str
    title: str
    html: str = """<!DOCTYPE html>
                <html>
                <body>
                </body>
                </html>"""


class PageInDB(Page):
    """Model for Page in database storage extends from Page"""
    disabled: Optional[bool] = False
    date_insert: Optional[datetime] = None
    date_update: Optional[datetime] = None
    username_insert: Optional[str] = None
    username_update: Optional[str] = None
