FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/face

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /face


RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock ./
RUN uv sync
# Копируем всё
COPY . .


RUN chmod +x /face/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "/face/entrypoint.sh"]
CMD ["python", "app/main.py"]