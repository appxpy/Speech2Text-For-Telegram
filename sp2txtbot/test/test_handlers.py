import pytest

from unittest.mock import AsyncMock
from db.models import User, Recognition
from handlers import Handlers
from aiogram.types import Message
from schema import msg


@pytest.mark.asyncio
async def test_start_handler(handlers):
    text_mock = "/start"
    message_mock = AsyncMock(text=text_mock)
    await handlers.start(message_mock)
    message_mock.answer.assert_called_with(msg('start'), parse_mode='Markdown', disable_web_page_preview=True)


@pytest.mark.filterwarnings("ignore:There is no current event loop")
@pytest.mark.asyncio
async def test_create_or_update_user_handler(handlers, initialize_db):
    text_mock = "test"
    message_mock = AsyncMock(text=text_mock)
    message_mock.from_user.id = 1
    await handlers.create_or_update_user(message_mock)
    assert await User.get(id=message_mock.from_user.id).values_list('id', flat=True) == 1


@pytest.mark.filterwarnings("ignore:coroutine 'AsyncMockMixin._execute_mock_call' was never awaited")
def test_register_handlers(handlers):
    assert handlers.register_handlers()


@pytest.mark.filterwarnings("ignore:There is no current event loop")
@pytest.mark.asyncio
async def test_media_handler_voice(handlers, voice_message, initialize_db, patch_speechkit):
    await handlers.media(voice_message)
    assert await User.get(id=voice_message.from_user.id).values_list('id', flat=True) == 1
    recognition = await Recognition.get(file_id=voice_message.voice.file_unique_id).prefetch_related('user')

    assert recognition
    assert recognition.recognized_text == 'Проверка'
    assert recognition.user.id == 1
    assert recognition.file_id == voice_message.voice.file_unique_id


@pytest.mark.filterwarnings("ignore:There is no current event loop")
@pytest.mark.asyncio
async def test_media_handler_video_note(handlers: Handlers, video_note_message: Message, initialize_db, patch_speechkit):
    await handlers.media(video_note_message)
    assert await User.get(id=video_note_message.from_user.id).values_list('id', flat=True) == 1
    recognition: Recognition = await Recognition.get(file_id=video_note_message.video_note.file_unique_id).prefetch_related('user')

    assert recognition
    assert recognition.recognized_text == 'Проверка'
    assert recognition.user.id == 1
    assert recognition.file_id == video_note_message.video_note.file_unique_id


@pytest.mark.filterwarnings("ignore:There is no current event loop")
@pytest.mark.asyncio
async def test_media_handler_voice_cache(handlers: Handlers, voice_message: Message, initialize_db, patch_speechkit):
    await handlers.create_or_update_user(voice_message)
    await handlers.cache_recognition(voice_message, 'Проверка', voice_message.voice.file_unique_id)

    await handlers.media(voice_message)
    assert await User.get(id=voice_message.from_user.id).values_list('id', flat=True) == 1
    recognition: Recognition = await Recognition.get(file_id=voice_message.voice.file_unique_id).prefetch_related('user')

    assert recognition
    assert recognition.recognized_text == 'Проверка'
    assert recognition.user.id == 1
    assert recognition.file_id == voice_message.voice.file_unique_id
