import asyncio
import logging
import tempfile
import settings
import time

from speechkit import auth, Session, RecognitionLongAudio
from typing import Iterable, List, Optional
from yc.entities import JWT, Chunk
from yc.utils import convert_ogg_to_mp3, convert_mp4_to_mp3
from pydantic import parse_obj_as


class Speech2Text:
    """
    Класс для распознавания речи, использующий speechkit для работы с Yandex SpeechKit
    """

    def __init__(self, logger: logging.Logger) -> None:
        self._jwt: Optional[JWT] = None
        self._session: Optional[Session] = None
        self.logger: logging.Logger = logger

    def _get_token(self) -> JWT:
        """
        Создает JWT токен для работы с Yandex SpeechKit, если он еще не создан или истек срок его действия

        :return: JWT токен
        :rtype: JWT
        """
        if not self._jwt or self._jwt.expiration < time.time():
            self._jwt = JWT(
                token=auth.generate_jwt(
                    service_account_id=settings.YANDEX_CLOUD_SERVICE_ACCOUNT_ID,
                    key_id=settings.YANDEX_CLOUD_PRIVATE_KEY_ID,
                    private_key=settings.YANDEX_CLOUD_PRIVATE_KEY.encode('utf-8')),
                created=time.time(),
                expiration=time.time() + 3600,
            )
        return self._jwt

    def _get_session(self) -> Session:
        """
        Создает сессию для работы с Yandex SpeechKit, если она еще не создана или срок действия JWT токена истек

        :return: Сессия для работы с Yandex SpeechKit
        :rtype: Session
        """
        if not self._session:
            self._session = Session.from_jwt(self._get_token().token)
        return self._session

    def _get_recognizer(self) -> RecognitionLongAudio:
        """
        Создает объект для распознавания речи, если он еще не создан или срок действия JWT токена истек

        :return: Объект для распознавания речи
        :rtype: RecognitionLongAudio
        """
        return RecognitionLongAudio(session=self._get_session(),
                                    service_account_id=settings.YANDEX_CLOUD_SERVICE_ACCOUNT_ID,
                                    aws_bucket_name=settings.YANDEX_CLOUD_BUCKET_NAME,
                                    )

    def _filter_chunks_by_channel(self, chunks: Iterable[Chunk]) -> Iterable[Chunk]:
        """
        Фильтрует объекты Chunk по каналу (channelTag == 1)

        :param Iterable[Chunk] chunks: Объекты Chunk, полученные от Yandex SpeechKit

        :return: Отфильтрованные объекты Chunk
        :rtype: Iterable[Chunk]
        """

        return filter(lambda x: x.channelTag == '1', chunks)

    def _parse(self, data: list) -> List[Chunk]:
        """
        Преобразует ответ от Yandex SpeechKit в объект STTResponse

        :param dict data: Ответ от Yandex SpeechKit

        :return: Список объектов Chunk
        :rtype: List[Chunk]
        """
        self.logger.info(f'Парсим ответ от Yandex SpeechKit - {data}')
        return parse_obj_as(List[Chunk], data)

    def _get_text_from_chunks(self, chunks: Iterable[Chunk]) -> str:
        """
        Получает текст из чанков

        :param Iterable[Chunk] chunks: Чанки
        :return: Текст
        :rtype: str
        """
        # Фильтруем чанки по каналу
        chunks = self._filter_chunks_by_channel(chunks)

        # Получаем все слова из всех объектов Alternative
        words = [word for chunk in chunks for alternative in chunk.alternatives for word in alternative.words]
        # Затем сортируем их по начальному времени
        words.sort(key=lambda x: float(x.startTime.replace('s', '')))
        # И возвращаем текст
        return ' '.join([word.word for word in words])

    async def _recognize(self, recognizer: RecognitionLongAudio) -> str:
        """
        Распознает речь и переводит ее в текст, используя Yandex SpeechKit

        :param RecognitionLongAudio recognizer: Распознаватель речи
        :return: Текст
        :rtype: str
        """
        self.logger.info('Распознавание речи запущено, ожидание результатов')

        while not recognizer.get_recognition_results():
            await asyncio.sleep(.5)  # pragma: no cover

        self.logger.info('Распознавание речи завершено, обработка результатов')

        data = self._parse(recognizer.get_data())

        print(data)

        if not data:
            return 'Текст не распознан'

        self.logger.info('Распознавание речи завершено, получение текста')

        text = self._get_text_from_chunks(data)

        self.logger.info('Распознавание речи завершено, текст получен - %s', text)

        return text

    async def recognize(self, audio: str, ext: str = '.ogg') -> str:
        """
        Распознает речь и переводит ее в текст, используя Yandex SpeechKit

        :param str audio: Аудиофайл в формате ogg/mp4
        :param str ext: Расширение файла (ogg - default / mp4 )
        :return: Текст
        :rtype: str
        """
        self.logger.info('Запуск распознавания речи')
        recognizer: RecognitionLongAudio = self._get_recognizer()
        with tempfile.NamedTemporaryFile(suffix='.mp3') as file:
            if ext == '.ogg':
                convert_ogg_to_mp3(audio, file.name)
            if ext == '.mp4':
                convert_mp4_to_mp3(audio, file.name)
            recognizer.send_for_recognition(
                file_path=file.name,
                literature_text=True,
                language_code='auto',
                model='general:rc',
                audioEncoding='MP3',
            )
        return await self._recognize(recognizer)
