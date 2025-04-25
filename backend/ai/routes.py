# ai/routes.py
import aiohttp
from fastapi import APIRouter, HTTPException, Depends, Path, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
from ai.gemini import generate_ai_content
from db import get_db
from schemas import ChatMessagesRequest, MessageResponse, PromptRequest, AIResponse, ChatResponse
from models import Message, User, Chat
from auth.security import get_current_user, oauth2_scheme
from sqlalchemy.future import select
from typing import List, Optional
import google.generativeai as genai
from config import settings
import asyncio

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/generate", response_model=AIResponse)
async def generate_ai_content_route(
    prompt: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    chat_id: Optional[int] = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(User).filter(User.id == current_user.id)
    result = await db.execute(query)
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        (generated_text, chat_id) = await generate_ai_content(prompt, image, chat_id, db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    return {"generated_text": generated_text, "chat_id": chat_id}

@router.get("/chats", response_model=List[ChatResponse])
async def get_user_chats_route(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    query = select(Chat).filter(Chat.user_id == current_user.id).order_by(Chat.created_at.desc())
    result = await db.execute(query)
    chats = result.scalars().all()
    return list(chats)

@router.get("/chats/{chat_id}", response_model=List[MessageResponse])
async def get_chat_messages_route(chat_id: int = Path(..., title="The ID of the chat to retrieve messages for"), current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    chat_query = select(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id)
    chat_result = await db.execute(chat_query)
    chat = chat_result.scalars().first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    messages_query = select(Message).filter(Message.chat_id == chat_id).order_by(Message.timestamp)
    messages_result = await db.execute(messages_query)
    messages = messages_result.scalars().all()
    return list(messages)