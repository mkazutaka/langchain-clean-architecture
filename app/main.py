from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.container import Container


def create_app():
    api_app = FastAPI()

    container = Container()

    api_app.container = container

    api_app.include_router(api_router, prefix="/v1")

    container.azure_chat_model()

    return api_app


app = create_app()


@app.exception_handler(RequestValidationError)
async def handler(_: Request, error: RequestValidationError):
    print(error.errors())
    print(error.body)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

