
import time
import random
from instagrapi import Client

cl = Client()
cl.login("Shamilier", "Shamil2004!")
# print(cl.account_info())
last_max_id = ''
followers = cl.user_followers(int(cl.user_id_from_username('Shamilier')), amount=15)
print(len(followers))
for i, j in followers.items():
    print(f'acc_id: {i}, ussername: {j.username}, full name: {j.full_name}')
