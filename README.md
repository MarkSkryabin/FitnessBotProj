🤖 Fitness Assistant Bot

Телеграм-бот на aiogram, который помогает следить за здоровьем и активностью:

💧 Учет воды

🍽 Подсчет калорий

🏋️ Учет тренировок

📊 Отображение дневного прогресса

⚙️ Персональный профиль пользователя

Бот автоматически рассчитывает дневные нормы калорий и воды, хранит данные в базе и обновляет статистику каждый день.

🚀 Возможности

✅ Настройка профиля (вес, рост, возраст, пол, активность, город)
✅ Автоматический расчет калорий и воды
✅ Логирование воды
✅ Учет съеденных калорий по продуктам
✅ Учет тренировок и сожженных калорий
✅ Визуальный прогресс-бар
✅ Хранение данных пользователя

📋 Команды бота
Команда	Описание
/start	Запуск бота
/help	Список команд
/set_profile	Настройка профиля
/profile	Просмотр профиля
/log_water <мл>	Учет воды
/log_food <продукт>	Учет калорий
/log_workout <тип> <мин>	Учет тренировки
/check_progress	Просмотр прогресса
🧱 Структура проекта (пример)
project/
│
├── bot.py
├── handlers.py
├── states.py
├── db.py
├── count_funcs.py
├── requirements.txt
├── .env
└── README.md

⚙️ Установка и запуск
1️⃣ Клонирование проекта
git clone https://github.com/your_username/your_repo.git
cd your_repo

2️⃣ Создание виртуального окружения
python -m venv venv


Активация:

Windows

venv\Scripts\activate


Linux / MacOS

source venv/bin/activate

3️⃣ Установка зависимостей
pip install -r requirements.txt


Пример requirements.txt:

aiogram==3.1.1
aiosqlite
python-dotenv
httpx

4️⃣ Настройка переменных окружения

Создай файл .env в корне проекта:

BOT_TOKEN=your_telegram_bot_token
API_TOKEN_WEATHER=your_api_key_if_used


❗ Файл .env не должен попадать в репозиторий.

5️⃣ Запуск бота
python bot.py

🌍 Деплой (Render)

Проект можно задеплоить на Render:

Тип сервиса: Web Service или Docker

Добавить переменные окружения в разделе Environment

Указать команду запуска:

python bot.py

🛠 Используемые технологии

Python 3.11

aiogram 3.x

aiosqlite

OpenWeatherAPI (для получения данных о продуктах / погоде)

📌 Автор

Марк Скрябин.