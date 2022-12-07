import logging
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
            self.logger.info('Получен голосовой файл')
            file = await message.voice.get_file()
            file = await file.download()
            self.logger.info('Файл скачан')
            # wait until file will be recognized
            text = await self.stt.recognize(file.name)
            self.logger.info('Файл распознан')
            await message.answer(text)  # type: ignore

    def register_handlers(self):
        # Регистрируем обработчики
        self.dp.register_message_handler(self.start, commands=['start'])
        self.dp.register_message_handler(self.media, content_types=['video_note', 'voice'])
        return True
