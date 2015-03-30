# Social Computing Tutorial #1
# Trending Topics
# It prints a result with JSON format
# author: webofthink@snu.ac.kr

import twitter
import credential

auth = twitter.oauth.OAuth(
	credential.getOAuthToken(),
	credential.getOAuthSecret(),
	credential.getConsumerKey(),
	credential.getConsumerSecret())
twitter_api = twitter.Twitter(auth=auth)

# Predefined ID
WORLD_WOE_ID = 1 
US_WOE_ID = 23424977
world_trends = twitter_api.trends.place(_id=WORLD_WOE_ID)
us_trends = twitter_api.trends.place(_id=US_WOE_ID)

# print world_trends
print
print us_trends
