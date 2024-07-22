import time
import random
from instagrapi import Client


def get_prev_followers(username, password, inst_acc_id, delay = 5):
    print(1)
    cl = Client()
    cl.login(username, password)
    print(2)

    followers = cl.user_followers(int(inst_acc_id))
    return followers
            

def monitor_new_followers(res, prev_followers):
    cl = Client()
    cl.login(res['username'], res['password'])

    # Сначала получаем всех текущих подписчиков
    previous_followers = set()
    last_max_id = ""

    try:
        while True:
            new_followers, last_max_id = cl.user_followers_v1_chunk(inst_acc_id, max_amount=50, max_id=last_max_id)
            current_followers = {(follower.pk, follower.username) for follower in new_followers}
            previous_followers.update(current_followers)
            
            if not last_max_id:  # Конец списка, все подписчики загружены
                print("Все текущие подписчики получены.")
                break
            else:
                print("Загрузка подписчиков...")
                time.sleep(3)

        # Время задержки для следующего запроса
        sleep_time = random.randint(delay-60, delay+60)
        print(f"Следующая проверка через {sleep_time} секунд.")
        time.sleep(sleep_time)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        time.sleep(300)
        