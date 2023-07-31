from langchain.chat_models.fake import FakeListChatModel

from app.entity.chat_message import ChatMessage, ChatMessageRole
from app.interactor.chat_interactor import ChatInteractor


def test_chat() -> None:
    chat_model = FakeListChatModel(
        responses=["fake responses"],
    )
    messages = [
        ChatMessage(role=ChatMessageRole.system, content="You are chat bot"),
        ChatMessage(role=ChatMessageRole.user, content="Hello"),
    ]
    interactor = ChatInteractor(
        chat_model=chat_model,
    )
    interactor.chat(messages, callbacks=[])
