import settings
import aiohttp
import time
import asyncio
import re
import logging
from aiohttp.client import ClientResponse
from pn.entities import PunctuationResponse

from pydantic import parse_obj_as


class Punctuator:
    """
    Класс для работы с API пунктуации
    """
    def __init__(self, logger: logging.Logger) -> None:
        self.user_id: int = settings.PUNCTUATION_USER_ID
        self.api_key: str = settings.PUNCTUATION_TOKEN
        self.send_url: str = "https://textovod.com/api/punctuation/user/add"
        self.status_url: str = "https://textovod.com/api/punctuation/user/status"
        self.logger: logging.Logger = logger
        self.CLEANR = re.compile('<.*?>')

    def _prepare_data_add(self, text: str) -> dict:
        """
        Подготавливает данные для запроса пунктуации

        :param str text: Текст

        :return: Данные
        :rtype: dict
        """
        return {
            "user_id": self.user_id,
            "api_key": self.api_key,
            "text": text,
            "lang": "ru",
        }

    def _prepare_data_status(self, text_id: str) -> dict:
        """
        Подготавливает данные для запроса статуса пунктуации

        :param str text_id: ID текста

        :return: Данные
        :rtype: dict
        """
        return {
            "text_id": text_id,
            "user_id": self.user_id,
            "api_key": self.api_key,
        }

    async def _parse_response(self, data: ClientResponse) -> PunctuationResponse:
        """
        Парсит ответ сервера

        :param ClientResponse data: Ответ сервера

        :return: Объект ответа сервера
        :rtype: PunctuationResponse
        """
        return parse_obj_as(PunctuationResponse, data)

    async def _send_request(self, url: str, data: dict) -> PunctuationResponse:
        """
        Отправляет запрос на сервер (асинхронно)

        :param str url: URL
        :param dict data: Данные

        :return: Ответ сервера
        :rtype: PunctuationResponse
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                response = await response.json()
                return await self._parse_response(response)

    def _clean_result(self, text: str) -> str:
        """
        Очищает текст от html-тегов

        :param str text: Текст

        :return: Текст без html-тегов
        :rtype: str
        """
        return re.sub(self.CLEANR, '', text)

    async def process(self, text: str) -> str:
        """
        Обрабатывает текст, добавляя к нему пунктуацию

        :param str text: Текст

        :return: Текст с пунктуацией
        :rtype: str
        """
        data = self._prepare_data_add(text)

        response = await self._send_request(self.send_url, data)

        self.logger.info("Отправлен запрос на пунктуацию, получен ID")
        text_id = response.text_id
        status = response.status
        start_time = time.time()
        while status != 2 or time.time() - start_time > 30:
            if not text_id:
                break
            data = self._prepare_data_status(text_id)
            response = await self._send_request(self.status_url, data)
            status = response.status
            await asyncio.sleep(1)
        if not response.punctuation:
            return text
        else:
            text = self._clean_result(response.punctuation)
            self.logger.info(f'Получен текст с пунктуацией: "{text}"')
            return text
