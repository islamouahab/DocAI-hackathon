from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from pydantic import BaseModel
from models import SubscriptionType


class SubscriptionResponse(BaseModel):
    id: Optional[int] = None
    type: SubscriptionType
    start_date: datetime
    end_date: Optional[datetime] = None
    is_active: bool

    class Config:
        from_attributes = True
        

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    subscription: Optional[SubscriptionResponse]

    class Config:
        from_attributes = True



class GeminiPrompt(BaseModel):
    prompt: str


class GeminiResponse(BaseModel):
    response: str



class PromptRequest(BaseModel):
    chat_id: Optional[int] = None
    prompt: str
    file: Optional[UploadFile] = None



class AIResponse(BaseModel):
    generated_text: str
    chat_id: int