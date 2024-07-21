
import time
import random
from instagrapi import Client

cl = Client()
cl.login("Shamilier", "Shamil2004!")
print(cl.account_info())
