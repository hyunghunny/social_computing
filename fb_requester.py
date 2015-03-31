# coding=UTF-8

##
# Facebook Graph API caller
# @brief There is two options to do: the one is using requests and the other is using facebook-sdk
# @author webofthink@snu.ac.kr
#

import requests
import json
import facebook
import urllib3
import urllib3.contrib.pyopenssl # due to https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning
urllib3.contrib.pyopenssl.inject_into_urllib3()
urllib3.disable_warnings()

class FacebookRequester:
    base_url = 'https://graph.facebook.com/'
    version = 'v2.3'
    content = []
    def __init__(self, token):
        self.access_token = token
        self.page = 'me'
    def setPage(self, page):
        self.page = page
    def getFeeds(self, limit, times):
        fields = 'feed.limit(%s)' % limit
        url = '%s/%s/%s?fields=%s&access_token=%s' % \
              (self.base_url, self.version, self.page, fields, self.access_token)
        counter = 0
        print url
        while counter < times:
            response = requests.get(url).json()
            print response

            try:
                content = response['feed']['data']
                paging = response['feed']['paging']
            except KeyError: # in case of retrieving by next page
                content = response['data']
                paging = response['paging']

            #print content
            #print paging

            self.content = self.content + content
            next_page_url = paging['next']
            if not next_page_url:
                break
            else :
                counter += 1
                url = next_page_url
                #print url
        return self.content

# Simple test
#ACCESS_TOKEN = 'CAACEdEose0cBAJdsINDvLIAksqZCEzKEksiUchhc4yl5aoP0wT2Bm55KMG0BZACpLYMNGrpnWI1mtuuPJMHcQR3jL2NvsrSOFi1xu6aKaGYNcpOSZCA0MF1PHSTmDfjKaA1q5UQQ6HYj79dfZCi8h63imMbE4PZBPBwlKj9ZCDCCXBwMnJDqyBn2c7YeIFwkxEQPeslrAWScWSU9YoWLIA'
#requester = FacebookRequester(ACCESS_TOKEN)
#requester.setPage('VisionMobile')
#feeds = requester.getFeeds(100, 5)
#print len(feeds)
#print json.dumps(feeds, indent=1)
#with open('feeds.json', 'w') as outfile:
#    json.dump(feeds, outfile)