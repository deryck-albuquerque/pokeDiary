from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class ResponseSchema(BaseModel, Generic[T]):
    detail: str
    result: Optional[T] = None
