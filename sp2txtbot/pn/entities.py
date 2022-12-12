from pydantic import BaseModel
from typing import Optional, Any


class PunctuationResponse(BaseModel):
    """
    Объект для хранения ответа API на запрос о пунктуации

    :param str text: Текст
    :param str punctuation: Пунктуация
    """
    status: int
    text_id: Optional[str]
    punctuation: Optional[str]
    result: Optional[Any]
    resultText: Optional[Any]
    text: Optional[str]
