FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY application ./application
COPY domain ./domain
COPY infrastructure ./infrastructure
COPY presentation ./presentation
COPY data ./data
COPY main.py ./

RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir .

CMD ["python", "main.py"]

