import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import setup_handlers
from middlewares import LoggingMiddleware
from db import init_db

# Создаём экземпляры бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Настраиваем middleware и обработчики
dp.message.middleware(LoggingMiddleware())
setup_handlers(dp)


async def main():
    await init_db()
    print("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
