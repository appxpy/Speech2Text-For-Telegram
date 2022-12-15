import settings
import logging

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils import executor
from handlers import Handlers
from tortoise import Tortoise

API_TOKEN = settings.BOT_TOKEN


logger = logging.getLogger('sp2txtbot')


class TelegramBot():
    def __init__(self, bot: Bot, dispatcher: Dispatcher):
        self.bot = bot
        self.dp = dispatcher
        self.dp.middleware.setup(LoggingMiddleware())
        self.handlers = Handlers(self.bot, self.dp, logger)

    async def on_startup(self, dp: Dispatcher) -> None:
        """
        Запуск бота, функция вызывается aiogram автоматически при запуске

        :param dp: Диспатчер
        :return:
        """

        if not self.handlers.register_handlers():
            logger.critical('Не удалось зарегистрировать обработчики')
            raise SystemExit(1)

        await Tortoise.init(db_url=settings.SQL_URL, modules={'models': ['db.models']})
        await Tortoise.generate_schemas()

        if settings.DEBUG:
            logger.warning('Бот запущен в режиме отладки')
            return

        if settings.BOT_SECURE_KEY:
            await self.bot.set_webhook(settings.BOT_WEBHOOK_URL, secret_token=settings.BOT_SECURE_KEY, drop_pending_updates=True)
            return

        await self.bot.set_webhook(settings.BOT_WEBHOOK_URL, drop_pending_updates=True)

    async def on_shutdown(self, dp: Dispatcher) -> None:
        """
        Завершение работы бота, функция вызывается aiogram автоматически при завершении работы

        :param dp: Диспатчер
        :return:
        """
        logger.warning('Завершение работы бота')

        # Удаляем вебхук
        if not settings.DEBUG:
            await self.bot.delete_webhook()

        await Tortoise.close_connections()
        logger.warning('Пока :)')

    def run(self):
        if settings.DEBUG:
            executor.start_polling(self.dp, on_startup=self.on_startup, on_shutdown=self.on_shutdown)
        else:
            executor.start_webhook(
                dispatcher=self.dp,
                webhook_path=f'/{settings.BOT_TOKEN_HASH}',
                on_startup=self.on_startup,
                on_shutdown=self.on_shutdown,
                skip_updates=True,
                host=settings.LISTEN,
                port=settings.VIRTUAL_PORT,
            )


if __name__ == '__main__':  # pragma: no cover
    bot = Bot(token=API_TOKEN)
    TelegramBot(bot, Dispatcher(bot)).run()
