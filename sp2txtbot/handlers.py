import logging

# Класс для обработки всех входящих сообщений
# Все обработчики должны быть асинхронными
# Все обработчики должны принимать два аргумента:
# 1. Объект бота
# 2. Объект сообщения


class Handlers:
    def __init__(self, bot, dp, logger):
        self.bot = bot
        self.dp = dp
        self.logger = logger

    async def start(self, message):
        self.logger.info('Получена команда /start')
        await message.answer('Привет, я бот!')

    async def media(self, message):
        await message.answer('Я умею обрабатывать видеосообщения')

    def register_handlers(self):
        # Регистрируем обработчики
        self.dp.register_message_handler(self.start, commands=['start'])
        self.dp.register_message_handler(self.media, content_types=['video_note', 'voice'])
        return True
