# coding=UTF-8

##
# Social Computing Tutorial #2-3:
#
# @brief Show % of tweets which contains hashtag and most used 10 hashtags with count  
#
# @author webofthink@snu.ac.kr
# 


import os.path
import json

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
# Examining Patterns in tweets
# @param tweets the JSON objects which had been retrieved
#
def exam_patterns(tweets) :
	status_texts = [ tweet['text']
		for tweet in tweets ]
	screen_names = [ tweet['user']['screen_name']
		for tweet in tweets ]
	hashtags = [ hashtag['text']
		for tweet in tweets
			for hashtag in tweet['entities']['hashtags'] ]

	# Compute a collection of all words from all tweets
	words = [ w
		for t in status_texts
			for w in t.split() ]
	
	# Make a return dictionary
	patterns = {}
	patterns['status_texts'] = status_texts
	patterns['screen_names'] = screen_names
	patterns['hashtags'] = hashtags
	patterns['words'] = words

	return patterns

##
# Calculate the rate of the tweets which have hashtags
# @param tweets the total tweets to be retrieved
#
def get_hashtags_rate(tweets):
	total_tweets = len(tweets)
	no_hash_tweets = 0
	for tweet in tweets :        
		hashtag = tweet['entities']['hashtags'] 
		if not hashtag :
			no_hash_tweets += 1
			
		hash_tweets = total_tweets - no_hash_tweets
	
	return (hash_tweets * 1.0) / (total_tweets * 1.0)

##
# Print hashtags which are most used
# @param patterns the pattern statistics
# @param count the number of hashtags to be shown.
#
def print_hashtags(patterns, count) :
	pt = PrettyTable(field_names=['Hashtag', 'Count'])
	c = Counter(patterns["hashtags"])
	for kv in c.most_common()[:count]:
		pt.add_row(kv)
	pt.align['Hashtag'], pt.align['Count'] = 'l', 'r' # Set column alignment
	print pt

# Simple test
statuses = get_tweets()

# Examine patterns of tweets
rate = get_hashtags_rate(statuses)
print " Hashtag contains tweet rate is " + str(rate)
print ""
 

# Show 10 Most Used Hashtags using prettytable
print "========================================================================="
print " 10 Most Used Hashtags "
print "========================================================================="
patterns = exam_patterns(statuses)
#print json.dumps(patterns["status_texts"][0:5], indent=1)
#print json.dumps(patterns["screen_names"][0:5], indent=1)
#print json.dumps(patterns["hashtags"][0:5], indent=1)
#print json.dumps(patterns["words"][0:5], indent=1)
print_hashtags(patterns, 10)


