import rospy
from std_msgs.msg import String
import os
import time


class Social:
    def __init__(self):
        self.vk_hashtag = str()
        self.twitter_hashtag = str()
        self.print_tags()

        sub_vk = rospy.Subscriber('/social/vk/newsfeed_scanner/hashtag', String, callback_vk_hashtag)
        twitter_vk = rospy.Subscriber('/social/twitter/code_scanner/code', String, callback_twitter_hashtag)
        
    def callback_vk_hashtag(self, data: String):
        self.vk_hashtag = data.data
        self.print_tags()

    def callback_twitter_hashtag(self, data: String):
        self.twitter_hashtag = data.data
        self.print_tags()

    def print_tags(self):
        clear = os.system('clear')
        print('-----------hashtags-----------')
        print('vk: ', self.vk_hashtag)
        print('twitter: ', self.twitter_hashtag)



if __name__ == '__main__':
    rospy.init_node('socials')
    social = Social()

    while True:
        try:
            rospy.get_master().getPid()
        except:
            break

        time.time(0.1)
