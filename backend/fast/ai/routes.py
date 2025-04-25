from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ai.gemini import generate_ai_content
from db import get_db
from schemas import PromptRequest, AIResponse
from models import User
from auth.security import get_current_user, oauth2_scheme
from sqlalchemy.future import select

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/generate", response_model=AIResponse)
async def generate_ai_content_route(data: PromptRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme),):
    query = select(User).filter(User.id == current_user.id)
    result = await db.execute(query)
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        (generated_text, chat_id) = await generate_ai_content(data, db, token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
    return {"generated_text": generated_text, "chat_id": chat_id}
