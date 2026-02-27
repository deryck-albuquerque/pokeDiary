from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class ResponseUsersSchema(BaseModel, Generic[T]):
    detail: str
    result: Optional[T] = None
