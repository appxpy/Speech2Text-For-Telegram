from typing import Optional, Union


schema = {
    'start': '👋 *Привет!*\nЯ бот для распознавания речи в голосовых сообщениях и кружочках)\n\n*🤔 Как этим пользоваться?*\nДля преобразования аудио в текст, тебе достаточно переслать мне голосовое сообщение или кружочек, я тут же возьмусь за работу). Обычно, распознавание не занимает много времени, примерно 10-30 секунд.\n\n*Бот выполнен в рамках проекта НИУ ВШЭ и имеет открытый исходный код.* [тык на меня](https://github.com/appxpy/Speech2Text-For-Telegram)\n\n made with ❤️ by @appxpy & @brazenoptimist',
    'processing': '🔁 *Обработка...*',
    'error': '❌ *Ошибка, попробуйте позже, а лучше напишите админам!!!*',
    'success': '✅ *Готово!*\n\n{message}',
}


def escape(text: str) -> str:
    return text.replace('_', '\\_').replace('*', '\\*').replace("[", "\\[").replace("`", "\\`")


class SafeFormat(dict):
    def __missing__(self, key):
        return key.join("")


def msg(key: Optional[str], **kwargs) -> str:
    """Возвращает сообщение из схемы по ключу"""

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
