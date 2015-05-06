# coding=UTF-8

##
# Social Computing Tutorial #3:
#
# @brief Simple Text Analytics with NLTK
#
# @author webofthink@snu.ac.kr
#

import os.path
import json
import sys
import nltk

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
# Tokenize all tweet messages
#
def tokenize(statuses) :
    status_texts = [ status['text']
        for status in statuses ]

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
        u'via',  u'...', u'!', u'``', u'http']

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
        if stem.find(u't.co') > 0:
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
statuses = get_tweets()
tokens = tokenize(statuses)
#print tokens
stemmed = get_stemmed_list(tokens)
#print stemmed
write_file('word.txt', stemmed)
