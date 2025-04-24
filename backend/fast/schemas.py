from pydantic import BaseModel
import uuid

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str

    class Config:
        from_attributes = True
