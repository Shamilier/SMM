
import time
import random
from instagrapi import Client

cl = Client()
cl.login("Space_phone__", "Shoma228!")


print(cl.media_info(3419916207215186534))
