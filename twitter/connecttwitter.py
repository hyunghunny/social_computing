# Social Computing Tutorial #1
# First Twitter Connection
# Copyright (C) 

import twitter
import credential

auth = twitter.oauth.OAuth(
	credential.getOAuthToken(),
	credential.getOAuthSecret(),
	credential.getConsumerKey(),
	credential.getConsumerSecret())
twitter_api = twitter.Twitter(auth=auth)

#print twitter_api