from typing import Optional
from pydantic import BaseModel


class ResponseModel(BaseModel):
    msg: Optional[str] = None
    code: Optional[int] = 0
