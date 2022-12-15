import pytest
from yc.stt import Speech2Text
from unittest.mock import Mock


@pytest.mark.asyncio
async def test_stt(patch_speechkit):
    stt = Speech2Text(
        logger=Mock(),
    )

    result = await stt.recognize('sp2txtbot/test/data/test-voice.ogg', '.ogg')

    assert result == 'проверка'


@pytest.mark.asyncio
async def test_stt_no_data(patch_speechkit):
    stt = Speech2Text(
        logger=Mock(),
    )
    stt._parse = Mock(return_value=None)
    result = await stt.recognize('sp2txtbot/test/data/test-voice.ogg', '.ogg')
    assert result == 'Текст не распознан'
