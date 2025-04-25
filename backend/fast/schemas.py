from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
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



class AIResponse(BaseModel):
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
    chat_id: int