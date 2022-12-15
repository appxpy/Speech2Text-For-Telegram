import pytest
from pn.punctuator import Punctuator
from pn.entities import PunctuationResponse
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from aiohttp import ClientResponse


@pytest.mark.asyncio
async def test_parse_response(monkeypatch):
    pn = Punctuator(
        logger=Mock(),
    )

    # # Patch aiohttp.ClientSession.post to avoid sending real request
    data = {
        'punctuation': 'Проверка',
        'status': 2,
        'text_id': '123',
        'result': None,
        'resultText': 'Проверка',
        'text': 'Проверка',
    }

    # resp = MockResponse(data, 200)

    # monkeypatch.setattr(ClientSession, 'post', MagicMock(return_value=resp))

    result = await pn._parse_response(data)  # type: ignore
    assert type(result) == PunctuationResponse
    assert result.punctuation == 'Проверка'


@pytest.mark.asyncio
async def test_punctuator(patch_punctuator):
    patch_punctuator()
    pn = Punctuator(
        logger=Mock(),
    )
    result = await pn.process('проверка')

    assert result == 'Проверка'


@pytest.mark.asyncio
async def test_punctuator_no_data(patch_punctuator):
    patch_punctuator(
        punctuation=None,
    )
    pn = Punctuator(
        logger=Mock(),
    )

    result = await pn.process('проверка')

    assert result == 'проверка'


@pytest.mark.asyncio
async def test_punctuator_no_text_id(patch_punctuator):
    patch_punctuator(
        status=1,
        punctuation=None,
        text_id=None,
    )

    pn = Punctuator(
        logger=Mock(),
    )

    result = await pn.process('проверка')

    assert result == 'проверка'


async def fake_send_request_no_text_id_on_second_run(url, data):
    if url.endswith('status'):
        return PunctuationResponse(
            punctuation='Проверка',
            status=2,
            text_id=None,
            result=None,
            resultText='Проверка',
            text='Проверка',
        )
    else:
        return PunctuationResponse(
            punctuation=None,
            status=1,
            text_id='123',
            result=None,
            resultText='Проверка',
            text='Проверка',
        )


@pytest.mark.asyncio
async def test_punctuator_no_text_id_on_second_run():
    pn = Punctuator(
        logger=Mock(),
    )
    pn._send_request = fake_send_request_no_text_id_on_second_run
    # Need to patch asyncio.sleep to avoid waiting for 1 second
    with patch('asyncio.sleep', new_callable=AsyncMock):
        result = await pn.process('проверка')
    assert result == 'Проверка'
