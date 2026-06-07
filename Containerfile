FROM python:3.12-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
COPY uv.lock /app/uv.lock

RUN pip install --no-cache-dir uv \
 && uv sync --frozen --no-dev

COPY . /app

# Reinstala/sincroniza con el código ya copiado para que no dependa de resolver nada al arrancar
RUN uv sync --frozen --no-dev

EXPOSE 8000
CMD ["/app/.venv/bin/uvicorn", "webapi.app:app", "--host", "0.0.0.0", "--port", "8000"]

