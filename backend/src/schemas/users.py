from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class UserBase(BaseModel):
    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

class UserRegister(UserBase):
    username: str = Field(..., min_length=1)
    pass

class UserLogin(UserBase):
    pass

class User(BaseModel):
    id: int