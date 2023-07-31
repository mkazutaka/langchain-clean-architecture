from typing import List

from pydantic.main import BaseModel

from app.entity.chat_message import ChatMessage


class Chat(BaseModel):
    model: str
    messages: List[ChatMessage]
    max_tokens: int
    temperature: float
    stream: bool
