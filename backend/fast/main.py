import asyncpg
from fastapi import FastAPI
from contextlib import asynccontextmanager
from config import settings

DATABASE_URL = settings.DATABASE_URL

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print(DATABASE_URL)
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.close()
        print("✅ PostgreSQL connection successful")
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
    yield

app = FastAPI(lifespan=lifespan)
