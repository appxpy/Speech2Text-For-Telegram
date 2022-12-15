FROM python:3.10-slim

WORKDIR /usr/src/sp2txtbot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y gcc python3-dev musl-dev postgresql build-essential netcat ffmpeg && \
    apt-get clean --dry-run && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip setuptools
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./entrypoint.sh .
RUN chmod +x /usr/src/sp2txtbot/entrypoint.sh

COPY . .

ENTRYPOINT ["/usr/src/sp2txtbot/entrypoint.sh"]