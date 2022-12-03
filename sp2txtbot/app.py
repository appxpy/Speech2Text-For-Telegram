import settings
import logging
import sys

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils import executor
from handlers import Handlers


API_TOKEN = settings.BOT_TOKEN


logger = logging.getLogger('sp2txtbot')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


async def on_startup(dp: Dispatcher):
    if not Handlers(bot, dp, logger).register_handlers():
        logger.critical('Не удалось зарегистрировать обработчики')
        sys.exit(1)

    if settings.DEBUG:
        logger.warning('Бот запущен в режиме отладки')
        return

    if settings.BOT_SECURE_KEY:
        await bot.set_webhook(settings.BOT_WEBHOOK_URL, secret_token=settings.BOT_SECURE_KEY, drop_pending_updates=True)
        return

    await bot.set_webhook(settings.BOT_WEBHOOK_URL, drop_pending_updates=True)
    # insert code here to run it after start


async def on_shutdown(dp: Dispatcher):
    logger.warning('Завершение работы бота')

    # Удаляем вебхук
    if not settings.DEBUG:
        await bot.delete_webhook()

    logger.warning('Пока :)')

if __name__ == '__main__':
    if settings.DEBUG:
        executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
    else:
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=f'/{settings.BOT_TOKEN_HASH}',
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=settings.LISTEN,
            port=settings.VIRTUAL_PORT,
        )
