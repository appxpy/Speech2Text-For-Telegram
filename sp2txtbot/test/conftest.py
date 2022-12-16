import pytest
import shutil

from handlers import Handlers
from unittest.mock import AsyncMock, Mock
from tortoise.contrib.test import finalizer, initializer, _TORTOISE_TEST_DB
from speechkit import RecognitionLongAudio, auth, Session
from pn.entities import PunctuationResponse
from pn.punctuator import Punctuator


@pytest.fixture(scope='session')
def patch_punctuator(monkeymodule):
    def patch_send_request(
        punctuation='Проверка',
        status=2,
        text_id='123',
        result=None,
    ):
        response = PunctuationResponse(
            punctuation=punctuation,
            status=status,
            text_id=text_id,
            result=result,
            resultText='Проверка',
            text='Проверка',
        )
        monkeymodule.setattr(Punctuator, '_send_request', AsyncMock(return_value=response))

    return patch_send_request


@pytest.fixture(scope='session')
def patch_speechkit(monkeymodule):
    def get_recognition_results(self):
        return True

    def get_data(self):
        return [{'alternatives': [{'words': [{'startTime': '0.560s', 'endTime': '1.459s', 'word': 'проверка', 'confidence': 1}], 'text': 'проверка', 'confidence': 1}], 'channelTag': '1'}]

    monkeymodule.setattr(RecognitionLongAudio, 'get_recognition_results', get_recognition_results)
    monkeymodule.setattr(RecognitionLongAudio, 'get_data', get_data)
    monkeymodule.setattr(RecognitionLongAudio, 'send_for_recognition', lambda *args, **kwargs: 'done')
    monkeymodule.setattr(RecognitionLongAudio, '__init__', lambda *args, **kwargs: None)

    def generate_jwt(*args, **kwargs):
        return 'test'

    monkeymodule.setattr(auth, 'generate_jwt', generate_jwt)
    session = Mock()
    session.folder_id = None
    session.token = 'test'
    monkeymodule.setattr(Session, 'from_jwt', session)


@pytest.fixture(scope='session')
def monkeymodule():
    with pytest.MonkeyPatch.context() as mp:
        yield mp


@pytest.fixture(scope="function")
def initialize_db(request):
    initializer(["db.models"], db_url=_TORTOISE_TEST_DB, app_label="models")
    request.addfinalizer(finalizer)


@pytest.fixture(scope='function')
def handlers():
    bot = AsyncMock()
    dispatcher = AsyncMock()
    logger = Mock()

    return Handlers(bot, dispatcher, logger)


async def mock_download_voice(destination_file):
    shutil.copyfile('sp2txtbot/test/data/test-voice.ogg', destination_file)


async def mock_download_video_note(destination_file):
    shutil.copyfile('sp2txtbot/test/data/test-video_note.mp4', destination_file)


async def mock_get_file_voice():
    file = AsyncMock()
    file.download = mock_download_voice
    return file


async def mock_get_file_video_note():
    file = AsyncMock()
    file.download = mock_download_video_note
    return file


def get_message():
    message = AsyncMock()
    message.from_user.id = 1
    message.from_user.first_name = 'test'
    message.from_user.last_name = 'test'
    message.from_user.username = 'test'
    message.from_user.full_name = 'test test'
    return message


@pytest.fixture(scope='function')
def voice_message():
    message = get_message()
    message.content_type = 'voice'
    message.voice.file_unique_id = 'test-voice'
    message.voice.get_file = mock_get_file_voice
    return message


@pytest.fixture(scope='function')
def video_note_message():
    message = get_message()
    message.content_type = 'video_note'
    message.video_note.file_unique_id = 'test-video_note'
    message.video_note.get_file = mock_get_file_video_note
    return message
