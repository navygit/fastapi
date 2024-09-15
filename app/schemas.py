
from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
import re


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    is_completed: bool
    owner_id: int

    class Config:
        orm_mode = True



class UserBase(BaseModel):
    username: str
    email: EmailStr

    @validator("username")
    def username_must_be_valid(cls, v):
        if not v or len(v) < 5:
            raise ValueError("Username must be at least 5 characters long.")
        return v

class UserCreate(UserBase):
    password: str

    @validator("password")
    def password_must_be_valid(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one number.")
        if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for char in v):
            raise ValueError("Password must contain at least one special character.")
        return v

class User(UserBase):
    id: int
    is_active: bool
    tasks: List["Task"] = []

    class Config:
        from_attributes = True  # Pydantic v2 replacement for orm_mode


