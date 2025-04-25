import google.generativeai as genai
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from schemas import PromptRequest
from models import User, Chat, Message, SubscriptionType
from config import settings
from auth.security import get_user_id_from_token
import asyncio
from sqlalchemy.orm import selectinload


loop = asyncio.get_event_loop()

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

async def generate_ai_content(data: PromptRequest, db: AsyncSession, token: str):
    userID = await get_user_id_from_token(token)
    userID = int(userID)
    user_result = await db.execute(select(User).where(User.id == userID).options(selectinload(User.subscription)))
    user = user_result.scalars().first()

    if not user:
        raise ValueError("User not found.")

    history = []
    current_chat = None

    if data.chat_id:
        chat_result = await db.execute(select(Chat).where(Chat.id == data.chat_id, Chat.user_id == userID))
        current_chat = chat_result.scalars().first()
        if not current_chat:
            raise ValueError("Chat not found.")
    else:
        current_chat = Chat(user_id=userID)
        db.add(current_chat)
        await db.commit()
        await db.refresh(current_chat)

    if user.subscription and user.subscription.type == SubscriptionType.premium:
        all_messages_result = await db.execute(
            select(Message)
            .join(Chat, Message.chat_id == Chat.id)
            .where(Chat.user_id == userID)
            .order_by(Message.timestamp)
        )
        all_messages = all_messages_result.scalars().all()
        history = [f"{'User' if msg.sender == 'user' else 'model'}: {msg.content}" for msg in all_messages]
    elif current_chat:
        message_result = await db.execute(
            select(Message).where(Message.chat_id == current_chat.id).order_by(Message.timestamp)
        )
        messages = message_result.scalars().all()
        history = [f"{'User' if msg.sender == 'user' else 'model'}: {msg.content}" for msg in messages]

    with open("AIrules.txt", "r") as file:
        rules = file.read()

    prompt_with_rules_and_history = ("Instructions:\n" + "\n".join(rules) + "\n\nChat History:\n" + "\n".join(history) + f"\n\nUser: {data.prompt}").replace("[[USERNAME]]", user.username)

    response = await loop.run_in_executor(None, model.start_chat(history=[]).send_message, prompt_with_rules_and_history)

    db.add_all([
        Message(chat_id=current_chat.id, sender="user", content=data.prompt),
        Message(chat_id=current_chat.id, sender="model", content=response.text.replace("[[USERNAME]]", user.username)),
    ])
    await db.commit()

    return (response.text.replace("[[USERNAME]]", user.username), current_chat.id)