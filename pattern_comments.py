from instagrapi import Client
import time

def send_direct_message_to_commenters(username, password, post_url, pattern, file_path):
    client = Client()
    client.login(username, password)

    # Получаем ID поста из URL
    media_id = client.media_id_from_url(post_url)

    # Получаем комментарии к посту
    comments = client.media_comments(media_id)

    # Фильтруем комментарии по паттерну
    target_users = [comment.user_id for comment in comments if pattern in comment.text]

    # Отправляем файл в директ каждому пользователю
    for user_id in target_users:
        client.direct_send(file_path, [user_id])
        print(f"Sent message to user ID: {user_id}")
        time.sleep(10)  # Пауза, чтобы избежать ограничений Instagram

# Использование функции
username = 'your_instagram_username'
password = 'your_instagram_password'
post_url = 'https://www.instagram.com/p/your_post/'
pattern = '+'
file_path = 'path_to_your_file'

send_direct_message_to_commenters(username, password, post_url, pattern, file_path)
