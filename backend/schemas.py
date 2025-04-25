# schemas.py
from datetime import datetime
from typing import Optional, List, Union
from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, HttpUrl
from models import SubscriptionType


class SubscriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = None
    type: SubscriptionType
    start_date: datetime
    end_date: Optional[datetime] = None
    is_active: bool


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: str
    subscription: Optional[SubscriptionResponse]



class GeminiResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    response: str



class PromptRequest(BaseModel):
    chat_id: Optional[int] = None
    prompt: Optional[str] = None
    image: Optional[UploadFile] = None


class AIResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    generated_text: str
    chat_id: int


class ChatResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    is_archived: bool


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    chat_id: int
    sender: str
    content: str
    timestamp: datetime


class ChatMessagesRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    chat_id: int


class IsPremiumResponse(BaseModel):
    is_premium: bool
