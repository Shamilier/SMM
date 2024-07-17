from instagrapi import Client
import config
import time
import random

cl = Client()
cl.login("Shamilier", "Shamil2004!")

class LikePost:
    def __init__(self, client) :
        self.cl = client
        self.tags = ['gamblingaddiction']
        self.commented_posts = []
        self.elapsed_time = 0
        print("Sucsessfully authorisade")
    def wait_time(self, delay):
        time.sleep(delay)
    def get_post_id_by_tag(self):
        medias = self.cl.hashtag_medias_recent(random.choice(self.tags), amount = 1)
        media_dict = medias[0].dict()
        print(media_dict)
        post_id = media_dict['id']
        return post_id
    
    def comment_post_by_tag(self, amount):
        for i in range(amount):
            post_id = self.get_post_id_by_tag()
            if post_id in self.commented_posts:
                pass
            else:
                comments = ['Cool!']
                self.cl.media_comment(post_id, comments[0])
                print(post_id)
                self.commented_posts.append(post_id)
                random_delay = random.randint(20, 60)
                print(f"Commened {len(self.commented_posts)}")
                self.wait_time(random_delay)
    def test(self):
        print("start_test")
        smth = self.cl.user_info_by_username('Shamilier')
        print(smth)
start = LikePost(cl)
start.test()
        
