from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    full_name: str = Field(...)
    email: EmailStr = Field(...)
    phone: str = Field(...)
    is_admin: bool = False

    class Config:
        schema_extra = {
            "example": {
                "username": "Joe Doe",
                "password": "any",
                "full_name": "Joe Doe",
                "email": "joe@xyz.com",
                "phone": "8-999-888-77-66",
                "is_admin": "False",
            }
        }


class UserRoleSchema(BaseModel):
    is_admin: bool = False

    class Config:
        schema_extra = {
            "example": {
                "is_admin": "False",
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "joe@xyz.com",
                "password": "any",
            }
        }


class UserUpdateSchema(BaseModel):
    username: Optional[str]
    password: Optional[str]
    full_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "username": "Joe Doe",
                "password": "any",
                "fullname": "Joe Doe",
                "email": "joe@xyz.com",
                "phone": "8-999-888-77-66",
            }
        }
