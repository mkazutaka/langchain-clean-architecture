from typing import Awaitable, List

from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models.base import BaseChatModel
from pydantic.main import BaseModel
from langchain.schema import (AIMessage, BaseMessage, HumanMessage, SystemMessage)

from app.entity.chat_message import ChatMessage


class ChatInteractor(BaseModel):
    chat_model: BaseChatModel

    def chat(
        self, messages: List[ChatMessage], callbacks: List[BaseCallbackHandler]
    ) -> Awaitable:
        # lc_messages = [m.to_langchain_message() for m in messages]

        return self.chat_model.apredict_messages(
            messages=[
                SystemMessage(content="aaaaaa")
            ],
            callbacks=callbacks,
        )
