from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    full_name: str
    password: str
    role: str = "USER"

    class Config:
        from_attributes = True

class UserLogin(UserBase):
    password: str

    class Config:
            from_attributes = True

class UserResponse(UserBase):
    id: int
    is_active: bool
    role: str
    created_at: datetime

    class Config:
        from_attributes = True