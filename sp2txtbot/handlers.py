import logging
import os
import tempfile
from yc.stt import Speech2Text
from aiogram import types

# Класс для обработки всех входящих сообщений
# Все обработчики должны быть асинхронными
# Все обработчики должны принимать два аргумента:
# 1. Объект бота
# 2. Объект сообщения


class Handlers:
    def __init__(self, bot, dp, logger):
        self.bot = bot
        self.dp = dp
        self.stt = Speech2Text(logger)
        self.logger = logger

    async def start(self, message):
        self.logger.info('Получена команда /start')
        await message.answer('Привет, я бот!')

    async def media(self, message: types.Message):
        if message.content_type == 'voice':
            ext = '.ogg'
            file = await message.voice.get_file()
        else:
            ext = '.mp4'
            file = await message.video_note.get_file()

        self.logger.info('Получен файл')

        # download file and make it temporary
        with tempfile.NamedTemporaryFile(suffix=ext) as file_path:
            self.logger.info(f'Сохраняем файл {file_path.name}')
            await file.download(destination_file=file_path.name)
            # send file to Yandex SpeechKit
            text = await self.stt.recognize(file_path.name, ext)
        await message.answer(text)

    def register_handlers(self):
        # Регистрируем обработчики
        self.dp.register_message_handler(self.start, commands=['start'])
        self.dp.register_message_handler(self.media, content_types=['video_note', 'voice'])
        return True
