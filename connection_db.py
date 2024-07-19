import mysql.connector

try:
    connection = mysql.connector.connect(
            host='monorail.proxy.rlwy.net',  # Адрес сервера базы данных, например 'localhost'
            port='31655',
            user='root',  # Имя пользователя
            password='OanUsGCwbkCbiPUcNubkbDVfVTnPPSbK',  # Пароль
            database='railway'  # Название базы данных
        )
    if connection:
        print("DB connected")

except Exception as e:
    print("Ошибочка(( проверь  правильность данных для подключения к бд")
    print(e)