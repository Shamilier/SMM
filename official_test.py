from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from instagrapi import Client
import asyncio
import csv
import io


from key_words_in_DM import monitor_direct_messages, keywords
from connection_db import connection
from db import Database
from secret import API_TOKEN
from check_followers import  get_prev_followers, check_followers_from_nickname, check_comments


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
        inst_id = client.user_id_from_username(name)
        
        db.add_inst_account(name, passw, user_id, inst_id)
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
        InlineKeyboardButton(text="get_followers", callback_data="get_followers"),
        InlineKeyboardButton(text="comments_checker", callback_data="comments_checker"),
        
    ]
    keyboard.add(*buttons)
    return keyboard


async def periodic_comments_check():
    while True:
        # Ждем 8 минут (480 секунд)
        await asyncio.sleep(600)
        await comments_checking()
        
        
async def comments_checking():
    print('зашел в функцию comments_checking')
    accs = db.get_comments_checking()
    for i in accs:
        check_comments(i)
        
        

async def periodic_followers_check():
    while True:
        # Ждем 8 минут (480 секунд)
        await asyncio.sleep(480)
        
        # Вызываем вашу функцию проверки подписчиков для всех нужных пользователей
        # Предполагаем, что функция subscribers_checking обрабатывает всех пользователей
        await followers_checking()
        
        
async def followers_checking():
    res = db.get_followers_check_list()
    for i in res:
        prev_followers = db.get_prev_followers(res['user_id'])
        print(prev_followers)
        # monitor_new_followers(res)
    

async def periodic_ping_db():
    while True:
        # Пингуем базу данных каждые 5 минут (300 секунд)
        await asyncio.sleep(600)
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            connection.commit()
        except Exception as e:
            print(f"Error pinging DB: {e}")

def check_post_url(url, username, password):
    try:
        cl = Client()
        cl.login(username, password)
        res= cl.media_pk_from_url(url)
        print(res)
        return res
        
    except Exception as e:
        print('smth wrong', e)
    


# ************************************************************
class Form(StatesGroup):
    waiting_for_instagram_username = State()
    waiting_for_instagram_password = State()
    account_added = State()
    waiting_for_greetning = State()
    waiting_for_acc_name_for_checking = State()
    waiting_for_acc_count_for_checking = State()
    waiting_for_posts_url = State()
    waiting_for_pattern = State()
    waiting_for_post_message = State()
    
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
    
# -=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-
    
@dp.callback_query_handler(lambda call: call.data == 'subscribers_checker')
async def subscribers_checker(call: CallbackQuery):
    await call.message.answer("Происходит загрузка подписчиков пожалуйста ждите")
    user_id = call.from_user.id
    res = db.get_username_password(user_id)
    print(res['username'], res['password'], res['inst_acc_id'])
    username, password, inst_acc_id = res['username'], res['password'], res['inst_acc_id']
    followers = get_prev_followers(username, password, int(inst_acc_id))
    for i, j in followers.items():
        await bot.send_message(user_id, f'acc_id: {i}, ussername: {j.username}, full name: {j.full_name}')
    db.update_followers(user_id, followers)
    await bot.send_message(user_id, f"У вас обнаружено {len(followers)} подписчиков. Теперь раз в 8 минут будет происходить мониторинг новых подписчиков. Вы можете отправлять каждому новому подписчику приветственное сообщение. Введите это сообщение слудующим сообщением. Если приветстовать не нужно, отправьте цифру 0. Что бы отключить функцию мониторинга отправьте команду /stop_followers")
    await Form.waiting_for_greetning.set()


@dp.message_handler(state=Form.waiting_for_greetning)
async def greetning_recieve(message: types.Message, state: FSMContext):
    status = message.text
    db.set_followers_checker(status, message.from_user.id)
    await bot.send_message(message.from_user.id, "Успешно добавлено!")
    await state.finish()

# -=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-

@dp.callback_query_handler(lambda call: call.data == 'get_followers')
async def get_followers(call: CallbackQuery):
    await bot.send_message(call.from_user.id, "Введите никнейм аккаунта у которого будем собирать подписчиков.")
    await Form.waiting_for_acc_name_for_checking.set()
    
@dp.message_handler(state=Form.waiting_for_acc_name_for_checking)
async def get_followers2(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['checking_username']= message.text
    await bot.send_message(message.from_user.id, "Теперь введите необходимое количество запрашиваемых подписчиков, чтобы собрать всех подписчиков отправьте 0")
    await Form.waiting_for_acc_count_for_checking.set()
    
@dp.message_handler(state=Form.waiting_for_acc_count_for_checking)
async def get_followers3(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['checking_count']= message.text
        await bot.send_message(message.from_user.id, "Отлично! В течение двух минут должен прийти файл-ответ.")
        # Получаем данные для входа в аккаунт из базы данных
        res = db.get_username_password(message.from_user.id)
        print(res)
        username, password, inst_acc_id = res['username'], res['password'], res['inst_acc_id']
        # Получаем список подписчиков
        followers = check_followers_from_nickname(username, password, data['checking_username'], data['checking_count'])
        # Сохраняем список подписчиков в CSV файл
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Username', 'Full Name'])  # Заголовки столбцов
        for id, follower in followers.items():
            writer.writerow([follower.username, follower.full_name])  # Данные подписчиков
        output.seek(0)  # Возвращаем указатель в начало файла
        # Преобразуем StringIO в BytesIO для отправки через Telegram
        bytes_output = io.BytesIO(output.read().encode('utf-8'))
        bytes_output.name = 'followers.csv'  # Назначаем имя файла
        bytes_output.seek(0)  # Возвращаем указатель в начало файла

        # Отправляем файл пользователю
        await bot.send_document(message.from_user.id, document=bytes_output, caption="Вот список подписчиков в формате CSV.")

        await state.finish()

# -=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-

@dp.callback_query_handler(lambda call: call.data == 'comments_checker')
async def comments_checker1(call: CallbackQuery):
    await bot.send_message(call.from_user.id, "Эта функция автоматизирует ответы на коментарии под постом. Отправьте ссылку на пост с Вашего аккаунта")
    await Form.waiting_for_posts_url.set()
    
@dp.message_handler(state=Form.waiting_for_posts_url)
async def comments_checker2(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['post_url']= message.text
        
        user_id = message.from_user.id
        res = db.get_username_password(user_id)
        data['username'] = res['username']
        data['password'] = res['password']
        data['inst_acc_id'] = res['inst_acc_id']
                
        pk = check_post_url(message.text, res['username'], res['password'])
        if pk:
            data['post_pk'] = pk
            await bot.send_message(message.from_user.id, "Теперь введите паттерн, на который будет реазировать скрипт")
            await Form.waiting_for_pattern.set()

@dp.message_handler(state=Form.waiting_for_pattern)
async def comments_checker3(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['pattern']= message.text
        await bot.send_message(message.from_user.id, "Теперь введите сообщение, которое будет отправлено пользователю")
        await Form.waiting_for_post_message.set()

@dp.message_handler(state=Form.waiting_for_post_message)
async def comments_checker4(message: types.Message, state:FSMContext):   
    async with state.proxy() as data:
        data['post_message'] = message.text
        db.update_comments_check(data['inst_acc_id'], data['username'], data['password'], data['pattern'], data['post_message'], data['post_pk'])
        await state.finish()
        await followers_checking()
        


        
        
        
    
    

    


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(periodic_ping_db())
    loop.create_task(periodic_followers_check())
    loop.create_task(periodic_comments_check())
    executor.start_polling(dp, skip_updates=True)



