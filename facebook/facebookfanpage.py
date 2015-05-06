# coding=UTF-8

##
# Social Computing Tutorial #4:
#
# @brief Simple Text Analytics with NLTK for generating word cloud on facebook.
#
# @author webofthink@snu.ac.kr
#

# – 자신이 좋아하는 페이지를 찾고 feed의 ‘message’를 수집
#– 전수업에 사용된 방법에 따라서 feed의 Word Cloud 작성
#– 가능하면 next를 이용한 pagination을 사용하세요
#– Word Cloud를 이미지로 저장/캡처해서 facebookfanpage.jpg로 제

import os.path
import json
import sys
import nltk

import jsonreader

from prettytable import PrettyTable
from fb_requester import FacebookRequester

##
# Get tweets from JSON dump file or twitter API
#
def get_feeds():
    file_path = "feeds.json"
    if os.path.exists(file_path):
        return jsonreader.read(file_path)
    else:
        ACCESS_TOKEN = 'CAACEdEose0cBAJdsINDvLIAksqZCEzKEksiUchhc4yl5aoP0wT2Bm55KMG0BZACpLYMNGrpnWI1mtuuPJMHcQR3jL2NvsrSOFi1xu6aKaGYNcpOSZCA0MF1PHSTmDfjKaA1q5UQQ6HYj79dfZCi8h63imMbE4PZBPBwlKj9ZCDCCXBwMnJDqyBn2c7YeIFwkxEQPeslrAWScWSU9YoWLIA'
        requester = FacebookRequester(ACCESS_TOKEN)
        requester.setPage('VisionMobile')
        feeds = requester.getFeeds(100, 5)
        return feeds


##
# Tokenize all feed messages
#
def tokenize(feeds):

    feed_texts = []
    for feed in feeds:
        try:
            feed_message = feed['description']
            feed_texts.append(feed_message)

        except KeyError:
            #print feed # if feed has no message field
            continue

    tokens = []
    for s in feed_texts:
        tokens += nltk.tokenize.word_tokenize(s.lower())
    return tokens

##
# Get stemmed list
#
def get_stemmed_list(tokens):
    from nltk.corpus import stopwords

    stop_words = stopwords.words('english') + ['.', ',', '--', '\'s', '?', ')', '(', ':', '\'', '\'re', '"',
                                               '-', '}', '{', u'—', 'rt', 'http', '%', 'co', '@', '#', '/', u'…',
                                               u'#', u';', u'amp', u't', u'co', u']', u'[', u'`', u'`', u'&', u'|',
                                               u'\u265b', u"''", u'$', u'//', u'/', u'%',
                                                                              u'via', u'...', u'!', u'``', u'http']

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
        #skip facebook things
        if stem.find(u'facebook.com') > 0:
            continue
        #skip http things
        elif stem.find(u'http') >= 0:
            #print stem
            continue
        else:
            stemmed.append(stem)
    return stemmed


def write_file(filename, lines):
    f = file(filename, 'w')
    for word in lines:
        try:
            f.write(word.encode('utf-8') + '\n')
        except UnicodeEncodeError, e:
            print 'Encoding error ' + word + '\n'
    f.close()

# Simple test
feeds = get_feeds()
tokens = tokenize(feeds)
#print tokens
stemmed = get_stemmed_list(tokens)
#print stemmed
write_file('feed-word.txt', stemmed)