import asyncio
import json
import logging
from typing import AsyncIterable, Awaitable

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain.schema.messages import BaseMessage

from app.container import Container
from app.entity.chat import Chat
from app.interactor.chat_interactor import ChatInteractor

router = APIRouter()


@router.post("/chat/completions")
@inject
async def create_chat_completions(
    chat: Chat,
    chat_interactor: ChatInteractor = Depends(
        Provide[Container.azure_chat_interactor]
    ),
):
    logging.info(f"Received request: {chat}")

    callback = AsyncIteratorCallbackHandler()

    if chat.stream:
        return StreamingResponse(
            _stream(
                chat_interactor.chat(
                    messages=chat.messages,
                    callbacks=[callback],
                ),
                callback=callback,
            ),
            media_type="text/event-stream",
        )
    else:
        res: BaseMessage = await chat_interactor.chat(
            messages=chat.messages,
            callbacks=[]
        )
        return JSONResponse(
            content=json.loads(res.json()),
        )


async def _stream(
    stream_fn: Awaitable,
    callback: AsyncIteratorCallbackHandler,
) -> AsyncIterable[str]:
    async def wrap_done(fn: Awaitable, event: asyncio.Event):
        try:
            await fn
        except Exception as e:
            print(f"Caught exception: {e}")
            raise e
        finally:
            event.set()

    task = asyncio.create_task(
        wrap_done(stream_fn, callback.done),
    )

    async for token in callback.aiter():
        # Match the format of the OpenAI response.
        data = json.dumps(
            {
                "choices": [
                    {
                        "delta": {"content": token},
                    }
                ]
            }
        )
        yield f"data: {data}\n\n"

    data = json.dumps(
        {
            "choices": [
                {
                    "finish_reason": "stop"
                }
            ]
        }
    )
    yield f"data: {data}\n\n"
    await task
