from pydantic import BaseModel, Field


class Result(BaseModel):
    message: str = "Status"