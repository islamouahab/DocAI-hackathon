import google.generativeai as genai
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from models import User, Chat, Message
from config import settings
from auth.security import get_user_id_from_token


genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")


async def generate_ai_content(data, db: AsyncSession, token: str):
    userID = await get_user_id_from_token(token)
    userID = int(userID)
    result = await db.execute(select(User).filter(User.id == userID))
    if data.chat_id:
        result = await db.execute(select(Chat).filter(
            and_(
                Chat.id == data.chat_id,
                Chat.user_id == userID
            )
        ))
        chat = result.scalars().first()
        if not chat:
            raise ValueError("Chat not found.")

        result = await db.execute(select(Message).filter(Message.chat_id == chat.id).order_by(Message.timestamp))
        messages = result.scalars().all()
        history = [
            f"{'User' if msg.sender == 'user' else 'Assistant'}: {msg.content}"
            for msg in messages
        ]
    else:
        chat = Chat(user_id=userID)
        db.add(chat)
        await db.commit()
        await db.refresh(chat)
        history = []

    with open("AIrules.txt", "r") as file:
        rules = file.read()

    prompt_with_rules_and_history = "Instructions:\n" + "\n".join(rules) + "\n\nChat History:\n" + "\n".join(history) + f"\n\nUser: {data.prompt}"

    current_chat = model.start_chat(history=[])
    response = current_chat.send_message(prompt_with_rules_and_history)

    db.add_all([
        Message(chat_id=chat.id, sender="user", content=data.prompt),
        Message(chat_id=chat.id, sender="model", content=response.text),
    ])
    await db.commit()

    return (response.text, chat.id)
