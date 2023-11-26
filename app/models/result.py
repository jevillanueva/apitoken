from pydantic import BaseModel, Field


class Result(BaseModel):
    """Model for Result, used in API operations, require message"""
    message: str = "Status"
