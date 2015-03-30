# coding=UTF-8

##
# Social Computing Tutorial #2-1:
#
# @brief Collect tweets by a specific hash tag
#
# @author webofthink@snu.ac.kr
# 

import twitter
import json
import credential

auth = twitter.oauth.OAuth(
	credential.getOAuthToken(),
	credential.getOAuthSecret(),
	credential.getConsumerKey(),
	credential.getConsumerSecret())

twitter_api = twitter.Twitter(auth=auth)


##
# Search tweets by hash tag
# @param query hash tag to search
# @param pages number of pages to iterate the search
# @param count number of item per request
# @return JSON object list
#
def search_tweets_by_hash_tag(query, pages, count):
	search_results = twitter_api.search.tweets(q=query, count=count)
	statuses = search_results['statuses']

	for _ in range(pages):	
		try:
			next_results = search_results['search_metadata']['next_results']
		except KeyError, e: # No more results when next_results doesn't exist
			print search_results['search_metadata']
			break
		kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
		search_results = twitter_api.search.tweets(**kwargs)
		statuses += search_results['statuses']
	return statuses;


# Simple test
#statuses = search_tweets_by_hash_tag('IoT', 5, 100)
#print json.dumps(statuses, indent=1)