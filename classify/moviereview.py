# coding=UTF-8

# Simple Supervised Learning Execution with builtin movie review corpus dataset of NLTK
# @author webofthink@snu.ac.kr
#
import random

import nltk
from nltk.corpus import movie_reviews


def printReviewInfo(file) :
    print movie_reviews.categories(file)
    print movie_reviews.words(file)

def getDocuments() :
    documents = [(list(movie_reviews.words(file)), category)
                 for category in movie_reviews.categories()
                 for fileid in movie_reviews.fileids(category)]
    random.shuffle(documents)
    return documents

# TODO document classification



# Simple Test

file_ids = movie_reviews.fileids()
file = file_ids[0]
#printReviewInfo(file)

document = getDocuments()
featuresets = [(document_features(d), c)for (d,c) in documents]
train_set = featuresets[100:]
test_set = featuresets[:100]

classifier = nltk.NaiveBayesClassifier.train(train_set)
print nltk.classify.accuracy(classifier, test_set)
classifier.show_most_informative_features(5)
gold = [tag for (features, tag) in test_set]
test = [classifier.classify(features) for features, tag in test_set]
cm = nltk.ConfusionMatrix(gold, test)
print cm.pp()
print cm.pp(sort_by_count=True, show_percents=True)

# Using Decision Tree Classifier

from nltk.corpus import movie_reviews
documents = [(list(movie_reviews.words(fileid)), category)
for category in movie_reviews.categories()
for fileid in movie_reviews.fileids(category)]
random.shuffle(documents)
all_words = nltk.FreqDist(w.lower()
for w in movie_reviews.words())
word_features = all_words.keys()[:600]

def document_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features

featuresets = [(document_features(d), c) for (d,c) in documents]
train_set = featuresets[100:]
test_set = featuresets[:100]
classifier = nltk.DecisionTreeClassifier.train(train_set)
nltk.classify.accuracy(classifier, test_set)
print classifier.pseudocode(depth=4)