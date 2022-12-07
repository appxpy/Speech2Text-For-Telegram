from dataclasses import dataclass
from enum import Enum, IntEnum, auto
from uuid import UUID
from typing import List, Optional, Literal, Type
from pydantic import BaseModel, Field, ValidationError, validator, constr, conlist


@dataclass(frozen=True)
class JWT:
    """
    Дата класс для хранения JWT токена

    :param string token: JWT токен
    :param float created: Время создания токена
    :param float expiration: Время истечения токена (1 час по умолчанию)
    """
    token: str
    created: float
    expiration: float


class Word(BaseModel):
    """
    Объект для хранения слова распознанной речи

    :param float startTime: Время начала слова
    :param float endTime: Время окончания слова
    :param str word: Слово
    :param float confidence: Уверенность ИИ в распознавании слова
    """
    startTime: str
    endTime: str
    word: str
    confidence: float


class Alternative(BaseModel):
    """
    Объект для хранения альтернативного варианта распознавания речи

    :param str text: Текст
    :param float confidence: Уверенность ИИ в распознавании текста
    :param List[Word] words: Список слов
    """
    text: str
    confidence: float
    words: List[Word]


class Chunk(BaseModel):
    """
    Объект для хранения чанка (куска) распознанной речи

    :param List[Alternative] alternatives: Список альтернативных вариантов распознавания
    :param str channelTag: Тэг канала
    """
    alternatives: List[Alternative]
    channelTag: str
