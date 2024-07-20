import logging
from mysql.connector import Error

class Database:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor(dictionary=True)
# ----------
    def add_user_if_not_exists(self, user_id):
        '''
        Добавляет пользователя в базу данных, если он еще не существует
        '''
        query = "INSERT IGNORE INTO users2 (user_id) VALUES (%s)"
        self.cursor.execute(query, (user_id,))
        self.connection.commit()
        if self.cursor.rowcount > 0:
            print("Новый пользователь был успешно добавлен.")
        else:
            print("Пользователь уже существует.")
        
# ----------
    
    def add_inst_account(self, username, passw, user_id, inst_id):        
        '''
        Добавлет данные аккаунта инстаграмм в таблицу inst_accounts
        '''
        query = """
            INSERT IGNORE INTO inst_accounts (user_id, username, password, inst_acc_id) 
            VALUES (%s, %s, %s);
        """      
        self.cursor.execute(query, (user_id, username, passw, inst_id))
        self.connection.commit()
# ----------
    def print_all_users(self):
        '''
        Извлекает и выводит все записи из таблицы users2.
        '''
        query = "SELECT * FROM users2"
        self.cursor.execute(query)
        result = self.cursor.fetchall()  # Извлекает все строки результата запроса

        if result:
            for user in result:
                print(user)  # Вывод информации о каждом пользователе
        else:
            print("Нет пользователей в базе данных.")
# ----------
    def get_int_accounts(self, user_id):
        query = "SELECT * FROM inst_accounts WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchall()
        return result
# ----------
    def check_account(self, user_id, username):
        query = "SELECT * FROM inst_accounts WHERE username = %s AND user_id = %s"
        self.cursor.execute(query, (username, user_id))
        result = self.cursor.fetchall()
        if len(result) > 0:
            return True
        return False
# ----------
    def get_username_password(self, user_id):
        query = "SELECT username, password FROM inst_accounts WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        return result
# ----------
    def update_followers(self, owner_id, current_followers):
        for follower in current_followers:
            # Добавляем owner_id в запрос и обновляем запрос для учёта этого параметра
            self.cursor.execute("""
                INSERT INTO followers (user_id, username, owner_id)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                username = VALUES(username), checked = CURRENT_TIMESTAMP;
            """, (follower[0], follower[1], owner_id))
        self.connection.commit()

        
        