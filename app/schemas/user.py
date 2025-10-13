"""
estructura de los datos de user
request - response
formato de links sugeridos proximos pasos
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List
from datetime import datetime


# schemas User
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    hashed_pwd: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserFavs(UserResponse):
    fav_stations_count: int

    model_config = ConfigDict(from_attributes=True)


# schemas Auth
class UserRegister(BaseModel):
    # los ... dice que es obligatorio
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    pwd: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    username: str
    pwd: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str | None = None  # Optional


# para las respuesta personalizadas con los links sugeriods (HATEOAS)
class UserMeResponse(BaseModel):
    user: UserResponse
    fav_stations_count: int
    links: dict

    model_config = ConfigDict(from_attributes=True)
