# coding=UTF-8

##
# Social Computing Tutorial #2-2:
#
# @brief Show 10 tweets which are most retweeted with prettytable
#
# @author webofthink@snu.ac.kr
# 

import os.path
import json
import sys

import collecttweets
import jsonreader

from collections import Counter
from prettytable import PrettyTable

##
# Get tweets from JSON dump file or twitter API
#
def get_tweets() :
	file_path = "tweets.json"
	if os.path.exists(file_path) :
		return jsonreader.read(file_path)
	else:
		return collecttweets.search_tweets_by_hash_tag('IoT', 5, 100)



##
# Print the most popular retweets
# @param tweets the tweets to be retrieved
# @param count the number of tweets to be shown
#
def print_popular_tweets(tweets, count):
	retweets_dup = [
		# Store out a tuple of these three values ...
		
		(tweet['retweet_count'],
			tweet['retweeted_status']['user']['screen_name'],
			tweet['text'])
		# ... for each status ...
		for tweet in tweets
		
		# ... so long as the status meets this condition.
		if tweet.has_key('retweeted_status')
	]
	retweets = list(set(retweets_dup))

	# Slice off the first 5 from the sorted results and display each item in the tuple
	pt = PrettyTable(field_names=['Count', 'Screen Name', 'Text'])
	for row in sorted(retweets, reverse=True)[:count]:
		pt.add_row(row)

	pt.max_width['Text'] = 50
	pt.align= 'l'
	print pt

# Simple test
statuses = get_tweets()

# Show Top 5 popular tweets
print_popular_tweets(statuses, 5)
