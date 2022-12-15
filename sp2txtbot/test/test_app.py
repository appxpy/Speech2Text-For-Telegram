import pytest
import app
import settings

from aiogram import Bot, Dispatcher
from unittest.mock import AsyncMock, MagicMock, PropertyMock, Mock


class AsyncPropertyMock(AsyncMock):  # pragma: no cover
    def _get_child_mock(self, /, **kwargs):
        return AsyncMock(**kwargs)

    async def __get__(self, obj, obj_type=None):
        return self()

    async def __set__(self, obj, val):
        self(val)

    def __await__(self):
        return self().__await__()


@pytest.fixture(scope='function')
def mock_bot(mocker):
    executor = MagicMock()
    mocker.patch('app.executor', executor)
    dispatcher = AsyncMock(spec=Dispatcher)
    bot = AsyncMock(spec_set=Bot)
    bot.me = AsyncPropertyMock()
    dispatcher.bot = bot
    dispatcher.middleware = MagicMock()
    app.settings.SQL_URL = 'sqlite://:memory:'
    return bot, dispatcher, executor


@pytest.fixture(scope='function')
def patch_db(mocker):
    db = mocker.patch('app.Tortoise', autospec=True)
    db.init.return_value = True
    return db


def test_app_run(mock_bot):
    bot, dispatcher, executor = mock_bot
    runner = app.TelegramBot(bot, dispatcher)
    assert not runner.run()
    assert executor.start_webhook.call_count == 1


def test_app_run_debug(mock_bot):
    bot, dispatcher, executor = mock_bot
    app.settings.DEBUG = True
    runner = app.TelegramBot(bot, dispatcher)
    assert not runner.run()
    assert executor.start_polling.call_count == 1
    app.settings.DEBUG = False


@pytest.mark.asyncio
async def test_on_startup_fail(mock_bot, patch_db):
    bot, dispatcher, executor = mock_bot
    dispatcher.register_message_handler.side_effect = Exception
    with pytest.raises(SystemExit):
        runner = app.TelegramBot(bot, dispatcher)
        assert not await runner.on_startup(dispatcher)
    assert bot.set_webhook.call_count == 0
    assert patch_db.init.call_count == 0


@pytest.mark.asyncio
async def test_on_startup(mock_bot, patch_db):
    bot, dispatcher, executor = mock_bot
    dispatcher.register_message_handler.return_value = True
    dispatcher.register_message_handler.side_effect = None
    app.settings.BOT_SECURE_KEY = None
    runner = app.TelegramBot(bot, dispatcher)
    assert not await runner.on_startup(dispatcher)
    assert runner.bot.set_webhook.call_count == 1
    assert patch_db.init.call_count == 1


@pytest.mark.asyncio
async def test_on_startup_secure(mock_bot, patch_db):
    bot, dispatcher, executor = mock_bot
    dispatcher.register_message_handler.return_value = True
    dispatcher.register_message_handler.side_effect = None
    app.settings.BOT_SECURE_KEY = 'test'
    runner = app.TelegramBot(bot, dispatcher)
    assert not await runner.on_startup(dispatcher)
    assert runner.bot.set_webhook.call_count == 1
    assert runner.bot.set_webhook.call_args[1]['secret_token'] == 'test'
    app.settings.BOT_SECURE_KEY = None
    assert patch_db.init.call_count == 1


@pytest.mark.asyncio
async def test_on_startup_debug(mock_bot, patch_db):
    bot, dispatcher, executor = mock_bot
    dispatcher.register_message_handler.return_value = True
    dispatcher.register_message_handler.side_effect = None
    app.settings.DEBUG = True
    runner = app.TelegramBot(bot, dispatcher)
    assert not await runner.on_startup(dispatcher)
    assert runner.bot.set_webhook.call_count == 0
    assert patch_db.init.call_count == 1
    app.settings.DEBUG = False


@pytest.mark.asyncio
async def test_on_shutdown(mock_bot, patch_db):
    bot, dispatcher, executor = mock_bot
    runner = app.TelegramBot(bot, dispatcher)
    assert not await runner.on_shutdown(dispatcher)
    assert patch_db.close_connections.call_count == 1
    assert runner.bot.delete_webhook.call_count == 1
