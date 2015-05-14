# coding=UTF-8

# Simple Supervised Learning Execution with builtin names corpus dataset of NLTK
# @author webofthink@snu.ac.kr
#
import random

import nltk


#nltk.download()
#names = nltk.corpus.names
from nltk.corpus import names

file_ids = names.fileids()
male_file = file_ids[0] # male.txt
female_file = file_ids[1] # female.txt

male_names = names.words(male_file)
female_names = names.words(female_file)


def getUniSexualNames() :
    uni_names =  [w for w in male_names if w in female_names ]
    return uni_names

def getLabeledNames() :
    all_names = ([(name, 'male') for name in names.words(male_file)] +
                 [(name, 'female') for name in names.words(female_file)])
    # names before shuffling
    #print all_names
    random.shuffle(all_names)
    return all_names

# TODO review this
def getSingleEndLetterFeatures(word) :
    return { 'last_letter' : word[-1] }

def getGenderFeatures(name) :
    features = {}
    features["first_letter"] = name[0].lower()
    features["last_letter"] = name[-1].lower()

    for letter in 'abcdefghijklmnopqrstuvwxyz' :
        features["count(%s)" % letter] = name.lower().count(letter)
        features["has(%s)" % letter] = (letter in name.lower())
    return features

def getFeatureSets(names, features):
    feature_sets = [ (features(n), g) for (n, g) in names ]
    return feature_sets

# Simple tests
#print getUniSexualNames()
all_names = getLabeledNames()

# features = getSingleEndLetterFeatures

feature_sets = getFeatureSets(all_names, getGenderFeatures)
train_set = feature_sets[500:]
test_set = feature_sets[:500]

classifier = classifier = nltk.NaiveBayesClassifier.train(train_set)

# Simple prediction
#print classifier.classify(features('Neo'))
#print classifier.classify(features('Trinity'))

# print prediction accuracy with a single end character
print nltk.classify.accuracy(classifier, test_set)
classifier.show_most_informative_features(5)