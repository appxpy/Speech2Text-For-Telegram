import os
import sys
import logging
import coloredlogs

from hashlib import sha512


# Общие настройки

DEBUG = bool(os.environ.get('DEBUG', False))
LISTEN = '0.0.0.0'
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# Задаем путь к файлу с логами, если он не существует, то создаем его

LOG_FILE = os.path.join(BASE_PATH, 'sp2txtbot.log')
if not os.path.exists(LOG_FILE):
    open(LOG_FILE, 'w').close()

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

if not BOT_TOKEN:
    logger.critical('Ошибка конфигурации: не указан токен бота')
    sys.exit(1)

BOT_TOKEN_HASH = sha512(BOT_TOKEN.encode()).hexdigest()                      # Хэш токена бота
BOT_SECURE_KEY = os.environ.get('BOT_SECURE_KEY')                            # Секретный ключ бота (для проверки вебхуков)
BOT_WEBHOOK_URL = f'https://{VIRTUAL_HOST}/{BOT_TOKEN_HASH}'                 # URL вебхука

# Настройки базы данных

SQL_ALLOWED_ENGINES = ['sqlite', 'postgresql']
SQLITE_DB_PATH = os.path.join(BASE_PATH, 'db.sqlite3')

if not os.path.exists(SQLITE_DB_PATH):
    open(SQLITE_DB_PATH, 'w').close()

SQL_ENGINE = os.environ.get('SQL_ENGINE', 'sqlite')  # Движок базы данных

if SQL_ENGINE not in SQL_ALLOWED_ENGINES:
    logger.critical('Ошибка конфигурации: недопустимый движок базы данных, допустимые движки: %s', ', '.join(SQL_ALLOWED_ENGINES))
    sys.exit(1)

SQL_DATABASE = os.environ.get('SQL_DATABASE')  # Имя базы данных
SQL_USER = os.environ.get('SQL_USER')          # Имя пользователя
SQL_PASSWORD = os.environ.get('SQL_PASSWORD')  # Пароль
SQL_HOST = os.environ.get('SQL_HOST')          # Хост
SQL_PORT = os.environ.get('SQL_PORT')          # Порт
