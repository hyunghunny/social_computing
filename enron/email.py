# coding=UTF-8

# mongodb manager
# @author webofthink@snu.ac.kr
#

import json
from datetime import datetime as dt

import pymongo # pip install pymongo
from bson import json_util # Comes with pymongo


def showSampleMessage(mbox):
    # Pick a message to look at…
    msg = mbox.find_one() # Display the message as pretty-­‐printed JSON. The use of
    # the custom serializer supplied by PyMongo is necessary in order
    # to handle the date field that is provided as a datetime.datetime
    # tuple.
    print json.dumps(msg,
        indent=1,
        default=json_util.default)


# Enron 직원들의 기록
def printEnronStats(mbox):
    senders = [ i for i in mbox.distinct("From")
        if i.lower().find("@enron.com") > -1 ]

    receivers = [ i for i in mbox.distinct("To")
        if i.lower().find("@enron.com") > -1 ]

    cc_receivers = [ i for i in mbox.distinct("Cc")
        if i.lower().find("@enron.com") > -1 ]

    bcc_receivers = [ i for i in mbox.distinct("Bcc")
        if i.lower().find("@enron.com") > -1 ]

    print "Num Senders:", len(senders)
    print "Num Receivers:", len(receivers)
    print "Num CC Receivers:", len(cc_receivers)
    print "Num BCC Receivers:", len(bcc_receivers)

# Query the database with the highly versatile "find" command,
# just like in the MongoDB shell.
def findMessagesByDate(mbox, start_date, end_date):
    query = mbox.find({
        "Date" :
            { "$lt": end_date,
              "$gt": start_date
            }
        }).sort("date")

    msgs = [ msg for msg in query ]

    print "Messages from a query by date range: " + str(start_date) + " ~ " + str(end_date)
    print json.dumps(msgs, indent=1, default=json_util.default)


# CEO의 이메일
def printCEOMsgs(mbox):
    aliases = ["kenneth.lay@enron.com",
        "ken_lay@enron.com",
        "ken.lay@enron.com",
        "kenneth_lay@enron.net",
        "klay@enron.com"] # More possibilities?

    to_msgs = [ msg for msg in mbox.find({"To" :
        { "$in": aliases } })]

    from_msgs = [ msg for msg in mbox.find({"From" :
        { "$in" : aliases } })]

    print "Number of CEO message sent to:", len(to_msgs)
    print "Number of CEO messages sent from:", len(from_msgs)


# Aggregation in MongoDB
# TODO fully understanding of aggregation is required
def showAllCEORecipients(mbox):
    results = mbox.aggregate([
		{"$match": {"From" :
			"kenneth.lay@enron.com"}
		},
		{"$project":
			{"From": 1, "To": 1, "Cc": 1, "Bcc": 1 }
		},
		{"$group":
			{"_id":	"$From",
			    "recipients": { "$addToSet" : "$To"   },
                "carbone_copy" : { "$addToSet" : "$Cc"   },
                "blind_carbone_copy" : { "$addToSet" : "$Bcc"   },
                }
			}

	])
    all_recipients = set()
    for r in results:

        for recipients in r["recipients"]:
            for to in recipients :
                all_recipients.add(to)
        for recipients in r["carbone_copy"]:
            for cc in recipients :
                all_recipients.add(cc)
        for recipients in r["blind_carbone_copy"]:
            for bcc in recipients :
                all_recipients.add(cc)
    print "all recipients of CEO mails: " + str(len(all_recipients))

# Analyzing Patterns in Sender/Recipient
def analyzePatterns(mbox):
    senders = [ i for i in mbox.distinct("From") ]
    receivers = [ i for i in mbox.distinct("To") ]
    cc_receivers = [ i for i in mbox.distinct("Cc") ]
    bcc_receivers = [ i for i in mbox.distinct("Bcc") ]

    print "Num Senders:", len(senders)
    print "Num Receivers:", len(receivers)
    print "Num CC Receivers:", len(cc_receivers)
    print "Num BCC Receivers:", len(bcc_receivers)

    # Set Operations for Enron Corpus
    senders = set(senders)
    receivers = set(receivers)
    cc_receivers = set(cc_receivers)
    bcc_receivers = set(bcc_receivers)

    # Find the number of senders who were also direct receivers
    senders_intersect_receivers = senders.intersection(receivers)

    # Find the senders that didn't receive any messages
    senders_diff_receivers = senders.difference(receivers)

    # Find the receivers that didn't send any messages
    receivers_diff_senders = receivers.difference(senders)

    # Find the senders who were any kind of receiver by
    # first computing the union of all types of receivers
    all_receivers = receivers.union(cc_receivers, bcc_receivers)
    senders_all_receivers = senders.intersection(all_receivers)

    print "Num senders in common with receivers:", len(senders_intersect_receivers)
    print "Num senders who didn't receive:", len(senders_diff_receivers)
    print "Num receivers who didn't send:", len(receivers_diff_senders)
    print "Num senders in common with *all* receivers:", len(senders_all_receivers)


def printRecipients(mbox, sender):
    # Get the recipient lists for each message
    recipients_per_message = mbox.aggregate([
        { "$match": {"From": sender } },
        {"$project": {"From": 1, "To": 1} },
        {"$group": {"_id": "$From", "recipients": {"$addToSet": "$To" } } }
    ]).next()['recipients']

    print "For " + sender + ":"
    # Collapse the lists of recipients into a single list
    all_recipients = [ recipient for message in recipients_per_message for recipient in message]
    print "Num all recipients:", len(all_recipients)

    # Calculate the number of recipients per sent message and sort
    recipients_per_message_totals = sorted([len(recipients) for recipients in recipients_per_message])
    print "Num recipients for each message:", recipients_per_message_totals

# Aggregate querying for counts of messages by date/time range
def printMessagesByRange(mbox):
    results = mbox.aggregate([{
            # Create a sub document called DateBucket with each date component projected
            # so that these fields can be grouped on in the next stage of the pipeline
            "$project": {
                "_id": 0,
                "DateBucket": {
                    "year" : { "$year" : "$Date"},
                    "month" : {"$month" : "$Date"},
                    "day" : {"$dayOfMonth" : "$Date"},
                    "hour" : {"$hour" : "$Date"},
                }
            }
        },
        {
            "$group": {
                # Group by year and date by using these fields for the key.
                "_id" : {"year": "$DateBucket.year",
                "month" : "$DateBucket.month"},
                # Increment the sum for each group by 1 for every document that's in it
                "num_msgs" : {"$sum" : 1}
            }
        },
        {
            "$sort" : {
                "_id.year": 1,
                "_id.month": 1
            }
        }
    ])

    for r in results: print r


# Simple test

# Connects to the MongoDB server
#client = pymongo.MongoClient()
client = pymongo.MongoClient('datascience.snu.ac.kr', 27017) # for using lab's db server

# Get a reference to the enron database
#db = client.enron

# Reference the mbox collection in the Enron database
mbox = client.enron.mbox # The number of messages in the collection
print "Number of messages in mbox: " + str(mbox.count())

# mysterious mails statistics
query = mbox.find({ "X-To": "" })
no_to_mails = [ msg for msg in query ]
print "# of mails which has no recipients: " + str(len(no_to_mails))
import re
query = mbox.find({"From" : { "$not": re.compile(r"^.*@enron\.com") } })
not_enron_domain_mails = [ msg for msg in query ]
print "# of mails which use not @enron.com as sender address : " + str(len(not_enron_domain_mails))
for mail in not_enron_domain_mails:
    print mail['From']
query = mbox.find({"To" : { "$not": re.compile(r"^.*@enron\.com") } })
not_enron_domain_mails = [ msg for msg in query ]
print "# of mails which use not @enron.com as sender address : " + str(len(not_enron_domain_mails))



# peer to peer mails
query = mbox.find({"To": {"$size" : 1 }})
peer_to_peer_mails =  [ msg for msg in query ]
print "# of mails which were sent peer to peer: " + str(len(peer_to_peer_mails))
private_mails =  [ i for i in peer_to_peer_mails
        if i['From'].lower().find("@enron.com") > -1 ]
print "# of private mails which were sent peer to peer: " + str(len(private_mails))

# Create a small date range here of one day
start_date = dt(2001, 4, 1) # Year, Month, Day
end_date = dt(2001, 4, 2) # Year, Month, Day

findMessagesByDate(mbox, start_date, end_date)
analyzePatterns(mbox)
printEnronStats(mbox)
showAllCEORecipients(mbox)

# print whom had been received from CEO
#printRecipients(mbox, "kenneth.lay@enron.com")
# print whom had been received from secretary
printRecipients(mbox, "rosalee.fleming@enron.com")

printMessagesByRange(mbox)
