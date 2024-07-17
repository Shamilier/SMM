from instagrapi import Client
import time

def fetch_followers(username_to_fetch, num_followers, delay):
    # Создаем клиент и логинимся
    client = Client()
    client.login('your_username', 'your_password')  # Введите здесь свои учетные данные

    # Получаем ID пользователя
    user_id = client.user_id_from_username(username_to_fetch)

    # Получаем подписчиков пользователя
    followers = []
    for follower in client.user_followers_chunk(user_id, amount=num_followers):
        followers.extend(follower)
        if len(followers) >= num_followers:
            break
        time.sleep(delay)  # задержка между запросами

    # Возвращаем список подписчиков
    return [follower.username for follower in followers[:num_followers]]

# Пример использования функции
followers_list = fetch_followers('target_username', 100, 5)  # Получить 100 подписчиков с задержкой в 5 секунд
print(followers_list)
