from aiogram.dispatcher.filters.state import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from instagrapi import Client
import asyncio


from key_words_in_DM import monitor_direct_messages, keywords
from connection_db import connection
from db import Database
from secret import API_TOKEN
from check_followers import  get_prev_followers


bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

db = Database(connection=connection)
# ************************************************************


def check_ins_acc(name, passw, user_id):
    try:
        client = Client()
        client.login(name, passw)
        
        db.add_inst_account(name, passw, user_id)
        return "success"
    except Exception as e:
        print(e)
        if e == 'challenge_required':
            return e
        return 'fail'

def get_account_action_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="DM checker", callback_data="DM"),
        InlineKeyboardButton(text="Auto comment", callback_data="auto_comment"),
        InlineKeyboardButton(text="Subscribers checker", callback_data="subscribers_checker"),
        
    ]
    keyboard.add(*buttons)
    return keyboard


async def periodic_subscriber_check():
    while True:
        # Ждем 8 минут (480 секунд)
        await asyncio.sleep(480)
        
        # Вызываем вашу функцию проверки подписчиков для всех нужных пользователей
        # Предполагаем, что функция subscribers_checking обрабатывает всех пользователей
        await subscribers_checking()
        
        
async def subscribers_checking():
    pass



# ************************************************************
class Form(StatesGroup):
    waiting_for_instagram_username = State()
    waiting_for_instagram_password = State()
    account_added = State()
    
@dp.message_handler(commands='accounts')
async def accs(message: types.Message):
    id = message.from_user.id
    accounts = db.get_accounts(id)

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    db.add_user_if_not_exists(message.from_user.id)
    db.print_all_users()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Добавить аккаунт Instagram", "Добавить Telegram канал")
    await message.answer("Выберите действие:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Добавить аккаунт Instagram")
async def add_instagram_account(message: types.Message):
    await Form.waiting_for_instagram_username.set()
    await message.reply("Введите имя пользователя Instagram:")

@dp.message_handler(state=Form.waiting_for_instagram_username)
async def instagram_username_received(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['instagram_username'] = message.text
    await Form.next()
    await message.reply("Введите пароль от аккаунта Instagram:")

@dp.message_handler(state=Form.waiting_for_instagram_password)
async def instagram_password_received(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await bot.send_message(user_id, 'Подождите пожалуйста пару секунд')

    # Извлекаем данные из состояния
    async with state.proxy() as data:
        if not db.check_account(user_id, data['instagram_username']):
            data['instagram_password'] = message.text
            check_result = check_ins_acc(data['instagram_username'], data['instagram_password'], user_id)
            if check_result == 'success':
                await message.reply("Аккаунт добавлен и проверен! Выберите действие с аккаунтом, если не знаете что делает каждая функция, то нажмите последнюю кнопку.", reply_markup=get_account_action_keyboard())
                await Form.account_added.set()
            elif check_result == 'fail':
                await message.reply("Не верный логин или пароль")
            elif check_result == 'challenge_required':
                await message.reply("Пожалуйста подтвердите вход в аккаунт через приложение Instagram Выберите действие с аккаунтом, если не знаете что делает каждая функция, то нажмите последнюю кнопку.", reply_markup=get_account_action_keyboard())
        else:
            await bot.send_message(user_id, 'Этот аккаунт уже был добавлен. Выберите действие с аккаунтом, если не знаете что делает каждая функция, то нажмите последнюю кнопку.', reply_markup=get_account_action_keyboard())

    await state.finish()
    
    
    
    
@dp.callback_query_handler(lambda call: call.data == 'subscribers_checker')
async def subscribers_checker(call: CallbackQuery):
    await call.message.answer("Происходит загрузка подписчиков пожалуйста ждите")
    user_id = call.from_user.id
    res = db.get_username_password(user_id)
    print(res['username'], res['password'])
    username, password = res['username'], res['password']
    followers = get_prev_followers(username, password)
    db.update_followers(followers)
    


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



