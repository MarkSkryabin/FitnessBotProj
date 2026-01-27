import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

# Чтение токена из переменной окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
API_TOKEN_WEATHER = os.getenv('API_TOKEN_WEATHER')
DB_PATH = os.getenv('DB_PATH')

if not BOT_TOKEN:
    raise ValueError('Переменная окружения BOT_TOKEN не установлена!')
if not API_TOKEN_WEATHER:
    raise ValueError('Переменная окружения API_TOKEN_WEATHER не установлена!')
if not DB_PATH:
    raise ValueError('Переменная окружения DB_PATH не установлена!')

