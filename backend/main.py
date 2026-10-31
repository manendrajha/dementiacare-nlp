from app.api.linking import router as linking_router
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import (
    connect_to_mongodb,
    close_mongodb_connection
)

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.memories import router as memories_router
from app.api.reminders import router as reminders_router
from app.api.conversations import router as conversations_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongodb()
    yield
    await close_mongodb_connection()


app = FastAPI(
    title="DementiaCare API",
    description="NLP-powered dementia support platform",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(auth_router)
app.include_router(memories_router)
app.include_router(reminders_router)
app.include_router(chat_router)
app.include_router(conversations_router)
app.include_router(linking_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to DementiaCare API",
        "status": "running"
    }


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected"
    }
