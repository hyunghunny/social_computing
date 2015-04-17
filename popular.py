# coding=UTF-8

##
# Social Computing Tutorial #4:
#
# @brief Show 10 Top likes feeds.
#
# @author webofthink@snu.ac.kr
#

import os.path
from collections import Counter
from prettytable import PrettyTable
import jsonreader
from fb_requester import FacebookRequester

##
# Get tweets from JSON dump file or twitter API
#
def get_feeds():
    file_path = "feeds.json"
    if os.path.exists(file_path):
        return jsonreader.read(file_path)
    else:
        ACCESS_TOKEN = 'CAACEdEose0cBAJdsINDvLIAksqZCEzKEksiUchhc4yl5aoP0wT2Bm55KMG0BZACpLYMNGrpnWI1mtuuPJMHcQR3jL2NvsrSOFi1xu6aKaGYNcpOSZCA0MF1PHSTmDfjKaA1q5UQQ6HYj79dfZCi8h63imMbE4PZBPBwlKj9ZCDCCXBwMnJDqyBn2c7YeIFwkxEQPeslrAWScWSU9YoWLIA'
        requester = FacebookRequester(ACCESS_TOKEN)
        requester.setPage('VisionMobile')
        feeds = requester.getFeeds(100, 5)
        return feeds


