from typing import Optional
import aiohttp
from fastapi import HTTPException, UploadFile
import google.generativeai as genai
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from schemas import PromptRequest
from models import User, Chat, Message, SubscriptionType, Attachment
from config import settings
from auth.security import get_user_id_from_token
import asyncio
import os
from sqlalchemy.orm import selectinload
import uuid

loop = asyncio.get_event_loop()
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

async def save_upload_file(upload_file: UploadFile) -> str:
    file_extension = os.path.splitext(upload_file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    try:
        with open(file_path, "wb") as file:
            while chunk := await upload_file.read(8192):
                file.write(chunk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving uploaded file: {e}")
    finally:
        await upload_file.close()
    return file_path

async def generate_ai_content(prompt: Optional[str], image: Optional[UploadFile], chat_id: Optional[int], db: AsyncSession, user: User):
    history = []
    current_chat = None

    # Check if chat_id is provided and valid
    if chat_id is not None and chat_id > 0:
        chat_result = await db.execute(select(Chat).where(Chat.id == chat_id, Chat.user_id == user.id))
        current_chat = chat_result.scalars().first()
        if not current_chat:
            current_chat = Chat(user_id=user.id)
            db.add(current_chat)
            await db.commit()
            await db.refresh(current_chat)
    else:
        current_chat = Chat(user_id=user.id)
        db.add(current_chat)
        await db.commit()
        await db.refresh(current_chat)

    if current_chat:
        message_result = await db.execute(select(Message).where(Message.chat_id == current_chat.id).order_by(Message.timestamp))
        messages = message_result.scalars().all()
        history = [f"{'User' if msg.sender == 'user' else 'model'}: {msg.content}" for msg in messages]

    with open("AIrules.txt", "r") as file:
        rules = file.read()

    prompt_parts = []
    prompt_text = ("Instructions:\n" + "\n".join(rules) + "\n\nChat History:\n" + "\n".join(history) + "\n\nUser: ")
    prompt_parts.append(prompt_text.replace("[[USERNAME]]", user.username))

    user_input_content = ""
    attachment_path = None
    attachment_type = None
    image_data = None

    if not prompt and not image:
        raise HTTPException(status_code=400, detail="No input provided")

    if prompt:
        prompt_parts.append(prompt)
        user_input_content = prompt

    if image:
        try:
            image_data = await image.read()
            file_path = await save_upload_file(image)
            attachment_path = file_path
            attachment_type = image.content_type
            prompt_parts.append({"mime_type": image.content_type, "data": image_data})
            user_input_content = f"Image: {image.filename}"
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing uploaded image: {e}")
        finally:
            await image.close()

    response = await loop.run_in_executor(None, model.generate_content, prompt_parts)
    response_text = response.text.replace("[[USERNAME]]", user.username) if response.text else ""

    message = Message(chat_id=current_chat.id, sender="user", content=user_input_content)
    db.add(message)
    await db.commit()
    await db.refresh(message)

    if attachment_path:
        attachment = Attachment(message_id=message.id, file_url=attachment_path, file_type=attachment_type)
        db.add(attachment)

    model_message = Message(chat_id=current_chat.id, sender="model", content=response_text)
    db.add(model_message)
    await db.commit()

    return (response_text, current_chat.id)