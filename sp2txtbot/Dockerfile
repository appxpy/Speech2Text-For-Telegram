FROM python:3.9.10-alpine

WORKDIR /usr/src/sp2txtbot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --update gcc python3-dev jpeg-dev zlib-dev musl-dev postgresql-dev build-base libstdc++ openssl && \
    rm -rf /var/cache/apk/*

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/sp2txtbot/entrypoint.sh
RUN chmod +x /usr/src/sp2txtbot/entrypoint.sh

RUN chmod +x /usr/src/sp2txtbot/entrypoint.sh

COPY . .

ENTRYPOINT ["/usr/src/sp2txtbot/entrypoint.sh"]