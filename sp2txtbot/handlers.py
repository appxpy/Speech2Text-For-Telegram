import logging
import os
import tempfile
import pickle
from typing import Optional
from yc.stt import Speech2Text
from aiogram import types, Bot, Dispatcher
from db.models import User, Recognition
from schema import msg


class Handlers:
    """
    Класс для всех обработчиков бота, включая команды
    """
    def __init__(self, bot: Bot, dp: Dispatcher, logger: logging.Logger):
        """
        Конструктор класса

        :param Bot bot: Объект бота
        :param Dispatcher dp: Диспатчер
        :param logging.Logger logger: Логгер

        :return:
        """
        self.bot: Bot = bot
        self.dp = dp
        self.stt = Speech2Text(logger)
        self.logger = logger

    async def start(self, message: types.Message):
        """
        Обработчик команды /start

        :param types.Message message: Сообщение

        :return:
        """
        await message.answer(msg('start'), parse_mode='Markdown', disable_web_page_preview=True)

    async def create_or_update_user(self, message: types.Message):
        defaults = {
            'tag': message.from_user.username,
            'username': message.from_user.full_name,
        }
        await User.update_or_create(id=message.from_user.id, defaults=defaults)

    async def cache_lookup(self, file_unique_id: str) -> Optional[str]:
        """
        Поиск распознанного текста в кэше

        :param str file_unique_id: Уникальный идентификатор файла

        :return Optional[str]: Текст или None
        """
        try:
            cached = await Recognition.get(file_id=file_unique_id)
            self.logger.info('Найдено в кэше')
            return cached.recognized_text
        except Exception:
            return None

    async def cache_recognition(self, message: types.Message, text: str, file_unique_id: str):
        """
        Сохранение распознанного текста в кэш

        :param types.Message message: Сообщение
        :param str text: Текст
        :param str file_unique_id: Уникальный идентификатор файла

        :return:
        """
        user = await User.get(id=message.from_user.id)
        cached = {
            'user': user,
            'file_id': file_unique_id,
            'recognized_text': text,
        }
        await Recognition.create(**cached)

    async def prepare_recognition(self, message: types.Message,) -> tuple:
        """
        Подготовка к распознаванию

        :param types.Message message: Сообщение

        :return str: Текст
        """
        # Скачиваем файл
        if message.content_type == 'voice':
            ext = '.ogg'
            file = await message.voice.get_file()
            file_unique_id = message.voice.file_unique_id
        else:
            ext = '.mp4'
            file = await message.video_note.get_file()
            file_unique_id = message.video_note.file_unique_id

        return file, file_unique_id, ext

    async def media(self, message: types.Message):
        """
        Обработчик медиафайлов - видео и голосовые сообщения

        :param types.Message message: Сообщение

        :return:
        """

        # Создаем или обновляем пользователя
        await self.create_or_update_user(message)

        # Отправляем сообщение о начале обработки
        _message = await self.bot.send_message(message.chat.id, msg('processing'), parse_mode='Markdown')

        # Определяем тип файла
        file, file_unique_id, ext = await self.prepare_recognition(message)

        # Проверяем наличие в кэше
        cache = await self.cache_lookup(file_unique_id)

        # Если есть в кэше, то отправляем из кэша
        if cache:
            await _message.edit_text(msg('success', message=cache), parse_mode='Markdown')
            return

        self.logger.info('Получен файл')

        # Скачиваем файл
        with tempfile.NamedTemporaryFile(suffix=ext) as file_path:
            self.logger.info(f'Сохраняем файл {file_path.name}')
            await file.download(destination_file=file_path.name)
            await file.download(destination_file='test' + ext)
            # Отправляем в STT (Speech2Text)
            text = await self.stt.recognize(file_path.name, ext)
        # Отправляем в Punctuator
        # text = await self.pn.process(text)
        # Сохраняем в кэш
        await self.cache_recognition(message, text, file_unique_id)
        # Отправляем пользователю
        await _message.edit_text(msg('success', message=text), parse_mode='Markdown')

    def register_handlers(self):
        # Регистрируем обработчики
        try:
            self.dp.register_message_handler(self.start, commands=['start'])
            self.dp.register_message_handler(self.media, content_types=['video_note', 'voice'])
        except Exception:
            return
        return True
