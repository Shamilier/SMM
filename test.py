
import time
import random
from instagrapi import Client

cl = Client()
cl.login("space_phone__", "Shoma228!")

print(cl.account_info())
