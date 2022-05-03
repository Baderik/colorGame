from pydantic import BaseModel, validator

from settings import RESPONSE_TYPES

__all__ = ["StandardModel"]


class StandardModel(BaseModel):
    type: str
    data: str = ""

    @validator("type")
    def standard_type(cls, v):
        if v in RESPONSE_TYPES:
            return v

        raise ValueError("type must be in the list")
