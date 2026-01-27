from pydantic import BaseModel
from typing import Optional, TypeVar

T= TypeVar('T')

class ResponseUsersSchema(BaseModel):
    detail: str
    result: Optional[T] = None