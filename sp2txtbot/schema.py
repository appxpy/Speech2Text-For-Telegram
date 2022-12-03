from typing import Optional, Union


schema = {
    'start': 'Тестовое сообщение. /start',
    'processing': 'Происходит обработка файла. Пожалуйста, подождите.',
    'error': 'Произошла ошибка. Попробуйте еще раз.',
    'success': 'Файл обработан - ваше сообщение: {message}',
}


def escape(text: str) -> str:
    return text.replace('_', '\\_').replace('*', '\\*').replace("[", "\\[").replace("`", "\\`")


class SafeFormat(dict):
    def __missing__(self, key):
        return key.join("")


def msg(key: Optional[str], **kwargs) -> str:
    """Returns message from scheme by key"""

    for k, v in kwargs.items():
        if isinstance(v, str):
            if not k.startswith('no_escape_') and k != 'no_escape_':
                kwargs[k.replace('no_escape_', '')] = escape(v)
    if not key:
        return ''
    if key in schema:
        return schema[key].format_map(SafeFormat(**kwargs))
    else:
        return "❌ Сообщение не найдено. Ключ: {key}".format_map(SafeFormat(key=key))
