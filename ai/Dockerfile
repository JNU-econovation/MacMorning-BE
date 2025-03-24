FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1

COPY . /ai

WORKDIR /ai

RUN uv sync --frozen --no-cache

CMD ["/ai/.venv/bin/uvicorn", "main:app", "--port", "8080", "--host", "0.0.0.0"]

