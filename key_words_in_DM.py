from instagrapi import Client
import datetime
import time
import random

def monitor_direct_messages(username, password, keywords, max_threads=10, delay=20):
    client = Client()
    client.login(username, password)
    
    last_checked = datetime.datetime.fromtimestamp(time.time())  # Инициализация времени последней проверки
    while True:
        print('---Новый цикл---')
        threads = client.direct_threads(amount=10, selected_filter="unread", thread_message_limit = 4) 
        for thread in threads:
            messages = client.direct_messages(thread.id)
            for message in messages:
                if message.timestamp >= last_checked:
                    # client.direct_message_seen(message.thread_id, message.id)
                    print('\n')
                    if (message.item_type == 'text'):
                        media = message.text
                        return f'Message from {client.username_from_user_id(message.user_id)}: {media}'
                    elif (message.item_type == 'clip'):
                        media = str(message.clip.video_url)
                        return media
                    print('\n')          
            last_checked = datetime.datetime.fromtimestamp(time.time())     # Обновляем время последней проверки
        time.sleep(int(random.uniform(0.7, 1.0) * delay))

# Использование функции
keywords = ['здравствуйте']  # Ключевые слова для поиска в сообщениях