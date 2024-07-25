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
        self.cursor = self.connection.cursor(buffered=True, dictionary=True)
        query = "INSERT IGNORE INTO users2 (user_id) VALUES (%s)"
        self.cursor.execute(query, (user_id,))
        self.connection.commit()
        if self.cursor.rowcount > 0:
            print("Новый пользователь был успешно добавлен.")
        else:
            print("Пользователь уже существует.")  
        self.cursor.close() 
# ----------
    def add_inst_account(self, username, passw, user_id, inst_id):        
        '''
        Добавлет данные аккаунта инстаграмм в таблицу inst_accounts
        '''
        self.cursor = self.connection.cursor(buffered=True, dictionary=True)
        query = """
            INSERT IGNORE INTO inst_accounts (user_id, username, password, inst_acc_id) 
            VALUES (%s, %s, %s, %s);
        """      
        self.cursor.execute(query, (user_id, username, passw, inst_id))
        self.connection.commit()
        self.cursor.close()
# ----------
    def print_all_users(self):
        '''
        Извлекает и выводит все записи из таблицы users2.
        '''
        self.cursor = self.connection.cursor(buffered=True, dictionary=True)
        query = "SELECT * FROM users2"
        self.cursor.execute(query)
        result = self.cursor.fetchall()  # Извлекает все строки результата запроса

        if result:
            for user in result:
                print(user)  # Вывод информации о каждом пользователе
        else:
            print("Нет пользователей в базе данных.")
        self.cursor.close()
# ----------
    def get_int_accounts(self, user_id):
        self.cursor = self.connection.cursor(buffered=True, dictionary=True)
        query = "SELECT * FROM inst_accounts WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchall()
        self.cursor.close()
        return result
    
# ----------
    def check_account(self, user_id, username):
        self.cursor = self.connection.cursor(buffered=True, dictionary=True)
        query = "SELECT * FROM inst_accounts WHERE username = %s AND user_id = %s"
        self.cursor.execute(query, (username, user_id))
        result = self.cursor.fetchall()
        self.cursor.close()
        if len(result) > 0:
            return True
        return False
# ----------
    def get_username_password(self, user_id):
        self.cursor = self.connection.cursor(buffered=True, dictionary=True)
        query = "SELECT username, password, inst_acc_id FROM inst_accounts WHERE user_id = %s"
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()
        self.cursor.close()
        return result
# ----------
    def update_followers(self, owner_id, current_followers):
        self.cursor = self.connection.cursor(buffered=True, dictionary=True)
        for follower_id, other in current_followers.items():
            # Добавляем owner_id в запрос и обновляем запрос для учёта этого параметра
            self.cursor.execute("""
                INSERT INTO followers (user_id, username, owner_id)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                username = VALUES(username), checked = CURRENT_TIMESTAMP;
            """, (follower_id, other.username, owner_id))
        self.connection.commit()
        self.cursor.close()
# ----------
    def set_followers_checker(self, status, user_id):
        self.cursor = self.connection.cursor(buffered=True, dictionary=True)
        query = 'UPDATE inst_accounts SET followers_checker = %s, greetning = %s WHERE user_id = %s'
        self.cursor.execute(query, (1, status, user_id))
        self.connection.commit()
        self.cursor.close()

# ----------
    def get_followers_check_list(self):
        self.cursor = self.connection.cursor(buffered=True, dictionary=True)
        query = 'SELECT * FROM inst_accounts WHERE followers_checker = %s'
        self.cursor.execute(query, (1,))
        try:
            result = self.cursor.fetchall()
            self.cursor.close()
            return result
        except Exception as e:
            print(e, 'smth wrong get_followers_check_list, db')
            self.cursor.close()
            return []
# ----------
    def get_prev_followers(self, user_id):
        self.cursor = self.connection.cursor(buffered=True, dictionary=True)
        query = "SELECT * FROM followers WHERE owner_id = %s"
        self.cursor.execute(query, (user_id,))
        try:
            result = self.cursor.fetchall()
            self.cursor.close()
            return result
        except Exception as e:
            print(e, 'smth wrong get_followers_check_list, db')
            self.cursor.close()
            return []
# ----------
    def update_comments_check(self, inst_acc_id, username, password, pattern, answer, pk):
        self.cursor = self.connection.cursor(buffered=True, dictionary=True)
        query = "INSERT INTO comments_check (inst_acc_id, username, password, pattern, answer, pk) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (inst_acc_id, username, password, pattern, answer, pk))
        self.connection.commit()
        self.cursor.close()
        return
        
# ---------
    def get_comments_checking(self):
        self.cursor = self.connection.cursor(buffered=True, dictionary=True)
        query = "SELECT * FROM comments_check"
        self.cursor.execute(query)
        try:
            result = self.cursor.fetchall()
            self.cursor.close()
            return result
        except Exception as e:
            print(e, 'smth wrong get_followers_check_list, db')
            self.cursor.close()
            return []
        