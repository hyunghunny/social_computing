# coding=UTF-8

##
# Social Computing Tutorial #10-2-1:
# Create Word Cloud with mail content
# @brief Simple Text Analytics with NLTK
#
# @author webofthink@snu.ac.kr
#

import os.path
import json
import sys
import nltk

import pymongo # pip install pymongo

from collections import Counter
from prettytable import PrettyTable


def get_ceo_mails_content(mbox) :
    aliases = ["kenneth.lay@enron.com",
    "ken_lay@enron.com",
    "ken.lay@enron.com",
    "kenneth_lay@enron.net",
    "klay@enron.com"] # More possibilities?

    from_msgs = [ msg for msg in mbox.find({"From" :
        { "$in" : aliases } })]

    # content stored message['parts'][]['content']
    contents = [ i['parts'][0]['content'] for i in from_msgs ]
    return contents

# Get content of private mails in enron company
#
def get_private_mails_content(mbox) :
    #  get all of content which was sent peer to peer from mbox
    query = mbox.find({"To": {"$size" : 1 }})
    peer_to_peer_mails =  [ msg for msg in query ]
    #print "# of mails which were sent peer to peer: " + str(len(peer_to_peer_mails))
    private_mails =  [ i for i in peer_to_peer_mails
            if i['From'].lower().find("@enron.com") > -1 ]
    # content stored message['parts'][]['content']
    contents = [ i['parts'][0]['content'] for i in private_mails ]
    return contents


##
# Tokenize all messages
#
def tokenize(contents) :
    status_texts = [ content for content in contents ]

    tokens = []
    for s in status_texts:
        tokens += nltk.tokenize.word_tokenize(s.lower())
    return tokens

##
# Get stemmed list
#
def get_stemmed_list(tokens) :
    from nltk.corpus import stopwords
    stop_words = stopwords.words('english') + ['.', ',', '--', '\'s', '?', ')', '(', ':', '\'', '\'re', '"',
        '-', '}', '{', u'—', 'rt', 'http', 't', 'co', '@', '#', '/', u'…',
        u'#', u';',  u'amp', u't', u'co', u']', u'[', u'`', u'`', u'&', u'|', u'\u265b', u"''", u'$', u'//', u'/'
        u'via',  u'...', u'!', u'``', u'http', u'%', ]

    from nltk.stem import PorterStemmer
    stemmer = PorterStemmer()
    stemmed = []
    for token in tokens:
        # try to decode token
        try:
            decoded = token.decode('utf8')
            #print decoded
        except UnicodeError:
            decoded = token

        if decoded is '' or decoded in stop_words:
            continue
        stem = stemmer.stem(decoded)
        #print stem
        # Skip a few text. I don't know why stopwords are not working :(
        #skip t.co things
        if stem.find(u'\\') > 0:
            continue
        if stem.find(u'/') > 0:
            continue
        #skip http things
        elif stem.find(u'http') >= 0:
            #print stem
            continue
        else:
            stemmed.append(stem)
    return stemmed

def write_file(filename, lines) :
    f = file(filename, 'w')
    for word in lines:
        try:
            f.write(word.encode('utf-8') + '\n')
        except UnicodeEncodeError, e:
            print 'Encoding error ' + word + '\n'
    f.close()

# Simple test
client = pymongo.MongoClient('datascience.snu.ac.kr', 27017) # for using lab's db server

# Get a reference to the enron database
#db = client.enron

# Reference the mbox collection in the Enron database
mbox = client.enron.mbox # The number of messages in the collection

#contents = get_private_mails_content(mbox)
contents = get_ceo_mails_content(mbox)

tokens = tokenize(contents)
#print tokens
stemmed = get_stemmed_list(tokens)
#print stemmed
write_file('word.txt', stemmed)
