from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.routes import router as auth_router
from routes.protected import router as protected_router
from ai.routes import router as ai_router

from db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()

    yield 

app = FastAPI(lifespan = lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(protected_router)
app.include_router(ai_router)