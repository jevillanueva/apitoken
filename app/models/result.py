from pydantic import BaseModel, Field


class Result(BaseModel):
    code: int = 0
    message: str = "Status"