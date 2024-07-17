from instagrapi import Client
import time

def auto_comment_on_new_posts(usernames, comment_text, check_interval=60):
    cl = Client()
    cl.login('your_username', 'your_password')

    # Словарь для отслеживания последнего поста каждого пользователя
    last_post_id = {username: None for username in usernames}

    while True:
        for username in usernames:
            posts = cl.user_medias(cl.user_id_from_username(username), 1)
            if not posts:
                continue  # Если постов нет, пропускаем

            latest_post = posts[0]
            if last_post_id[username] is None or latest_post.id != last_post_id[username]:
                print(f"Новая публикация от {username}, добавляем комментарий...")
                cl.media_comment(latest_post.id, comment_text)
                last_post_id[username] = latest_post.id
            else:
                print(f"Нет новых публикаций от {username}")

        print("Ожидание следующей проверки...")
        time.sleep(check_interval)

# Использование функции
usernames = ['user1', 'user2', 'user3', 'user4', 'user5']
comment_text = "Привет! Классный пост!"
auto_comment_on_new_posts(usernames, comment_text)
