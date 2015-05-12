# coding=UTF-8

# Simple Supervised Learning Execution with Reuter data set
# @author webofthink@snu.ac.kr
#

from reuter import loadReuterDataSet
import nltk

def getAuthorFeatures(author) :
    features = {}
    # TODO return appropriate features

def getFeatureSets(names, features):
    feature_sets = [ (features(n), g) for (n, g) in names ]
    return feature_sets


def getNaiveBayesClassifier(train_set) :
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    return classifier

authors = ['AaronPressman', 'AlanCrosby', 'AlexanderSmith', 'BenjaminKangLim', 'BernardHickey']
# TODO get data set of 5 authors which are sorted with ascending order
dataset = loadReuterDataSet("train", authors)
print len(dataset)
# TODO get all articles with shuffling
all_articles = None

# TODO stemming and stopwords handling
stemmed = None

# TODO labeling with author name

# TODO learn with Naive Bayesian Classifier

# TODO What is the most informative feature?
