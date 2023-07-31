from fastapi import APIRouter

from app.api.v1 import chat_completions, models

api_router = APIRouter()

api_router.include_router(chat_completions.router)
api_router.include_router(models.router)
