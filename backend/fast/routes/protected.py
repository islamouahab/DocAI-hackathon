from datetime import datetime
from sqlalchemy.orm import joinedload
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from models import User
from schemas import IsPremiumResponse, UserResponse, SubscriptionResponse, SubscriptionType
from auth.security import get_current_user
from sqlalchemy.future import select


router = APIRouter(prefix='/api')


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    query = select(User).options(joinedload(User.subscription)).filter(User.id == current_user.id)
    
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    subscription = user.subscription if user.subscription else SubscriptionResponse(
        id=None,
        type=SubscriptionType.free,
        start_date=datetime.utcnow(),
        end_date=None,
        is_active=True
    )

    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        subscription=subscription
    )



@router.get("/is_premium", response_model=IsPremiumResponse)
async def is_premium(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    query = select(User).options(joinedload(User.subscription)).filter(User.id == current_user.id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    is_premium_status = user.subscription and user.subscription.type == SubscriptionType.premium and user.subscription.is_active
    return IsPremiumResponse(is_premium=is_premium_status)