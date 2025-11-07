from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator

# User Schemas


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    def validate_password(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Password cannot be empty")
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        if len(v) > 100:
            raise ValueError("Password must be less than 100 characters")
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
    user_id: int | None = None


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
    updated_at: datetime | None

    class Config:
        from_attributes = True


class ShareLinkCreate(BaseModel):
    # snippet_id: int
    expires_hours: int | None = 24
    password: str | None = None

    class Config:
        from_attributes = True


class ShareLinkResponse(BaseModel):
    id: int
    token: str
    expires_at: datetime | None
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
    password: str | None = None
