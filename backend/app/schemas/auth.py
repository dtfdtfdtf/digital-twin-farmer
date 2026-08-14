# app/schemas/auth.py
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional


class UserRegister(BaseModel):
    """Schema for user registration"""
    email: EmailStr = Field(..., description="Email address")
    username: str = Field(..., min_length=3, max_length=50, description="Username")
    password: str = Field(..., min_length=6, max_length=100, description="Password")
    full_name: str = Field(..., min_length=1, max_length=100, description="Full name")
    role: str = Field("farmer", description="User role: farmer, officer, admin")
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload"""
    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None