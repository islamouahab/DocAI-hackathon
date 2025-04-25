from datetime import datetime, timedelta

from jose import JWTError, jwt
from sqlalchemy import select
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from models import User
from config import settings
from db import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def hash_password(password: str):
	return pwd_context.hash(password)


async def verify_password(plain_password: str, hashed_password: str):
	return pwd_context.verify(plain_password, hashed_password)


async def create_access_token(data: dict):
	to_encode = data.copy()
	expires = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expires, "token_type": "bearer"})
	return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
	)
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
		user_id: str = payload.get("sub")
		if user_id is None:
			raise credentials_exception
	except JWTError:
		raise credentials_exception

	result = await db.execute(select(User).where(User.id == int(user_id)))
	user = result.scalars().first()
	if user is None:
		raise credentials_exception
	return user


async def get_user_id_from_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is not None:
            return user_id
        else:
            return None
    except JWTError:
        print("Invalid token")
        return None 
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
