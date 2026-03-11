from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str

class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class LoginUser(BaseModel):
    email: EmailStr
    password: str
