FROM python:3.10-slim AS build
WORKDIR /app

RUN pip install poetry

# Poetry設定
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/

# 依存関係のインストール
RUN poetry install --no-dev

FROM python:3.10-slim
WORKDIR /app

RUN pip install gunicorn

COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY . /app

CMD exec gunicorn --bind :8000 app.main:app -k uvicorn.workers.UvicornWorker
