from schema import msg


def test_msg_exists():
    message = 'test'
    assert msg('success', message=message) == f'✅ *Готово!*\n\n{message}'


def test_msg_not_exists():
    assert msg('not_exists') == '❌ Сообщение не найдено. Ключ: not_exists'


def test_invalid_key():
    assert msg('success', k='v') == '✅ *Готово!*\n\n'


def test_key_is_none():
    assert msg(None) == ''
