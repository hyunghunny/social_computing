# coding=UTF-8

# mongodb handling example for aggregation
# @author webofthink@snu.ac.kr
#

import pymongo # pip install pymongo


# Connects to the MongoDB server
client = pymongo.MongoClient()
# Get a reference to the enron database
db = client.zipcode

# Reference the mbox collection in the Enron database
zipcodes = db.zipcode # The number of messages in the collection

# TODO $match and $group

# TODO Return states with populations above 10 million
db.zipcodes

# TODO Return average city population by state

# TODO Return largest and smallest cities by state: Group and Sort

# TODO Return largest and smallest cities by state: Second group & Projection

# TODO Aggregation with user preference data

# TODO $unwind and $addtoset

# TODO Return the five most common ‘likes’
