from enum import Enum

from langchain.schema import (AIMessage, BaseMessage, HumanMessage, SystemMessage)
from pydantic.main import BaseModel


class ChatMessageRole(str, Enum):
    user = "user"
    system = "system"
    ai = "assistant"


class ChatMessage(BaseModel):
    role: ChatMessageRole
    content: str

    def to_langchain_message(self) -> BaseMessage:
        if self.role == ChatMessageRole.ai:
            return AIMessage(content=self.content)
        if self.role == ChatMessageRole.user:
            return HumanMessage(content=self.content)
        if self.role == ChatMessageRole.system:
            return SystemMessage(content=self.content)
        raise ValueError(f"Invalid role: {self.role}")
