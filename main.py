from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import asyncio

from key_words_in_DM import monitor_direct_messages, keywords
from connection_db import connection
from db import Database




API_TOKEN = '7428146964:AAHLkbopN-1NBwmJ2SMlcTP65i4kpBpzU6c'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

db = Database(connection=connection)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(f"Привет! Введи логин Instagram аккаунта")

@dp.message_handler()
async def echo(message: types.Message):
    await message.reply(f"Ваш Chat ID: {message.chat.id}")
async def check_direct_messages(dp: Dispatcher):
    # Здесь должны быть логин и пароль для Instagram
    username = 'Shamilier'
    password = 'Shamil2004!'
    while True:
        video_url = monitor_direct_messages(username, password, keywords)
        if video_url and video_url.startswith('http'):
            await bot.send_video('1297355532', video=video_url)
        await asyncio.sleep(10)  # Делаем задержку перед следующей проверкой

async def on_startup(dp):
    asyncio.create_task(check_direct_messages(dp))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
