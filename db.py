import logging
from aiogram import Bot, Dispatcher, executor, types
import markups as nav
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from psycopg2.extras import DictCursor
import json
from connection_db import connection


class Database:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor(cursor_factory=DictCursor)

    def add_user(self, user_id):
        '''
        Данная функция добавлет пользователя в базу данных
        '''
        self.cursor.execute("SELECT 1")
        with self.connection as cur:
            tmp = f"INSERT INTO users (user_id) VALUES ({user_id});"
            result = self.cursor.execute(tmp)
            self.connection.commit()
            return result

    def user_exists(self, user_id):
        '''
        Данная функция проверяет, существует ли пользователь с ,
        заданным user_id базе данных
        '''
        self.cursor.execute("SELECT 1")
        with self.connection:
            tmp = f"SELECT * FROM users WHERE user_id = {user_id}"
            self.cursor.execute(tmp)
            result = self.cursor.fetchall()
            return bool((len(result)))
        
    def get_signup(self, user_id):
        '''
        Данная функция проверяет информацию о том, 
        зарегестрирован пользователь или нет
        '''
        self.cursor.execute("SELECT 1")
        with self.connection:
            tmp = f"SELECT sign_up FROM users WHERE user_id = {user_id}"
            self.cursor.execute(tmp)
            result = self.cursor.fetchall()
            for row in result:
                sign_up = row['sign_up']
            return sign_up