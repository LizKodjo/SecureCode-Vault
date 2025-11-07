from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

# User Schemas


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Password cannot be empty')
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        if len(v) > 100:
            raise ValueError('Password must be less than 100 characters')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Token Schemas


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None

# Snippet schemas


class SnippetBase(BaseModel):
    title: str
    language: str
    code: str


class SnippetCreate(SnippetBase):
    pass


class SnippetResponse(SnippetBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class ShareLinkCreate(BaseModel):
    # snippet_id: int
    expires_hours: Optional[int] = 24
    password: Optional[str] = None

    class Config:
        from_attributes = True


class ShareLinkResponse(BaseModel):
    id: int
    token: str
    expires_at: Optional[datetime]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class SharedSnippetResponse(BaseModel):
    title: str
    language: str
    code: str
    shared_at: datetime


class ShareAccessRequest(BaseModel):
    password: Optional[str] = None
