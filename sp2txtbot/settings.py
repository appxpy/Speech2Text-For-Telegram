import os
import sys
import logging
import coloredlogs
import base64

from hashlib import sha512


# Общие настройки

DEBUG = bool(os.environ.get('DEBUG', False))
LISTEN = '0.0.0.0'
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# Задаем путь к файлу с логами, если он не существует, то создаем его

LOG_FILE = os.path.join(BASE_PATH, 'sp2txtbot.log')
open(LOG_FILE, 'w+').close()

# Задаем конфигурацию логгера

_ = None

if not DEBUG:
    _ = LOG_FILE

coloredlogs.install()

logging.basicConfig(
    filename=_,
    format='[%(asctime)s] - [%(levelname)s] - %(name)s - %(message)s',
    level=logging.DEBUG if DEBUG else logging.INFO
)

logger = logging.getLogger(__name__)

# Настройки прокси

VIRTUAL_HOST = os.environ.get('VIRTUAL_HOST', '')             # Виртуальный хост
VIRTUAL_PORT = os.environ.get('VIRTUAL_PORT', 8080)           # Виртуальный порт


# Настройки бота

BOT_TOKEN = os.environ.get('BOT_TOKEN', '')  # Токен бота
BOT_TOKEN_HASH = sha512(BOT_TOKEN.encode()).hexdigest()                      # Хэш токена бота
BOT_SECURE_KEY = os.environ.get('BOT_SECURE_KEY')                            # Секретный ключ бота (для проверки вебхуков)
BOT_WEBHOOK_URL = f'https://{VIRTUAL_HOST}/{BOT_TOKEN_HASH}'                 # URL вебхука

# Настройки базы данных

SQL_ALLOWED_ENGINES = ['sqlite', 'postgres']
SQLITE_DB_PATH = os.path.join(BASE_PATH, 'db.sqlite3')

open(SQLITE_DB_PATH, 'w+').close()

SQL_ENGINE = os.environ.get('SQL_ENGINE', 'sqlite')  # Движок базы данных

SQL_DATABASE = os.environ.get('SQL_DATABASE')  # Имя базы данных
SQL_USER = os.environ.get('SQL_USER')          # Имя пользователя
SQL_PASSWORD = os.environ.get('SQL_PASSWORD')  # Пароль
SQL_HOST = os.environ.get('SQL_HOST')          # Хост
SQL_PORT = os.environ.get('SQL_PORT')          # Порт

if SQL_ENGINE == 'sqlite':
    SQL_URL = f'{SQL_ENGINE}:///{SQLITE_DB_PATH}'
else:  # pragma: no cover
    SQL_URL = f'{SQL_ENGINE}://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DATABASE}'
# Настройки Yandex SpeechKit

YANDEX_CLOUD_BUCKET_NAME = os.environ.get('YANDEX_CLOUD_BUCKET_NAME', '')  # Имя бакета
YANDEX_CLOUD_SERVICE_ACCOUNT_ID = os.environ.get('YANDEX_CLOUD_SERVICE_ACCOUNT_ID', '')  # Идентификатор сервисного аккаунта
YANDEX_CLOUD_PRIVATE_KEY_ID = os.environ.get('YANDEX_CLOUD_PRIVATE_KEY_ID', '')  # Приватный ключ сервисного аккаунта
YANDEX_CLOUD_PRIVATE_KEY_BASE64 = os.environ.get('YANDEX_CLOUD_PRIVATE_KEY_BASE64', '')  # Приватный ключ сервисного аккаунта (в base64)
YANDEX_CLOUD_PRIVATE_KEY = base64.b64decode(YANDEX_CLOUD_PRIVATE_KEY_BASE64).decode()  # Приватный ключ сервисного аккаунта (в base64)


# Настройки сервиса автоматической пунктуации

PUNCTUATION_USER_ID = int(os.environ.get('PUNCTUATION_USER_ID', 0))  # Идентификатор пользователя
PUNCTUATION_TOKEN = os.environ.get('PUNCTUATION_TOKEN', '')      # Токен пользователя
