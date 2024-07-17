import time
import random

def monitor_new_followers(cl, user_id):
    previous_followers = set(cl.user_followers(user_id))
    
    while True:
        current_followers = set(cl.user_followers(user_id))
        new_followers = current_followers - previous_followers
        
        if new_followers:
            print(f"Новые подписчики: {new_followers}")
            # Здесь можно добавить дополнительные действия
        
        previous_followers = current_followers
        
        # Случайный интервал от 2 до 5 минут
        sleep_time = random.randint(120, 300)
        print(f"Следующая проверка через {sleep_time} секунд")
        time.sleep(sleep_time)
