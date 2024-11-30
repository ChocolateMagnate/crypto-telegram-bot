FROM python:3.11-slim
LABEL authors="Vlad Korol"

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ARG TELEGRAM_TOKEN
ARG OPENAI_API_KEY
ENV TELEGRAM_API_TOKEN=$TELEGRAM_TOKEN
ENV OPENAI_API_KEY=$OPENAI_API_KEY

CMD ["sh", "-c", "PYTHONPATH=/app python -m bot"]