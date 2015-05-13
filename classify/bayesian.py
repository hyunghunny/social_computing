# coding=UTF-8

# Simple Supervised Learning Execution with Reuter data set
# @author webofthink@snu.ac.kr
#

from reuter import loadReuterDataSet
import nltk
import random
##
# add stemmed_text property of doc in data set
#
def addStemmedText(dataset) :
    for doc in dataset :

        all_content = " ".join([doc['text']])
        tokens = all_content.split()
        stemedList = getStemmedList(tokens)
        #stemmed_text = " ".join(stemedList)
        doc['stemmed_text'] = stemedList

def strip(token) :
    strip_tokens = ['(', ')', ',', '.', '\'', '"']
    for strip_token in strip_tokens :
        # XXX: risky but fancy method to remove strip tokens
        token = token.replace(strip_token, '')
        #while (token in strip_token) :
        #    token = token.strip(strip_token)
    return token

def isNumber(s):
    try:
        float(s) # for int, long and float
    except ValueError:
        try:
            complex(s) # for complex
        except ValueError:
            return False

    return True
##
# Get stemmed list
#
def getStemmedList(tokens) :
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

        stem = stemmer.stem(decoded)
        stem = strip(stem)

        if isNumber(stem) :
            continue

        if stem is '' :
            continue
        if stem in stop_words:
            continue
        if stem.find(u'http') >= 0:

            continue
        else:
            stemmed.append(stem)

    # print stemmed
    return stemmed


def getDocumentFeatures(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features


def getLabeledArticles(dataset) :
    all_pairs = ([(list(doc['stemmed_text']), doc['author']) for doc in dataset])
    # all_pairs before shuffling
    #print all_pairs
    random.shuffle(all_pairs)
    return all_pairs

def getFeatureSets(names, features):
    feature_sets = [ (features(n), g) for (n, g) in names ]
    return feature_sets


def getNaiveBayesClassifier(train_set) :
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    return classifier


def getAllWords(dataset) :
    words_list = []
    for doc in dataset :
        all_content = " ".join(doc['stemmed_text'])
        tokens = all_content.split()
        text = nltk.Text(tokens)
        fdist = text.vocab()

        # Common words that aren't stopwords
        words = [w for w in fdist.keys() \
            if w.lower() not in nltk.corpus.stopwords.words('english')]

        # Long words that aren't URLs
        # [w for w in fdist.keys() if len(w) > 15 and not w.startswith("http")]

        for word in words :
            words_list.append(word)

    all_words = nltk.FreqDist(w.lower() for w in words_list)

    return all_words

# Simple test

authors = ['AaronPressman', 'AlanCrosby', 'AlexanderSmith', 'BenjaminKangLim', 'BernardHickey']
# get data set of 5 authors which are sorted with ascending order
train_dataset = loadReuterDataSet("train", authors)
test_dataset = loadReuterDataSet("test", authors)
addStemmedText(train_dataset) # add a "stemmed_text" property which is stemmed
addStemmedText(test_dataset)

# get all stemmed words in the data set
all_words = getAllWords(train_dataset)
print "Number of all words: " + str(len(all_words))
word_features = all_words.keys()[:100]

# show word list
#for feature in word_features :
#    print feature[:50]

train_pairs = getLabeledArticles(train_dataset) # labeling with author name
test_pairs = getLabeledArticles(test_dataset) # labeling with author name

#for pair in  train_pairs:
#    print pair[1]

print "Number of pairs: " + str(len(train_pairs))


train_feature_sets = getFeatureSets(train_pairs, getDocumentFeatures)
test_feature_sets = getFeatureSets(test_pairs, getDocumentFeatures)

train_set = train_feature_sets
print len(train_set)
test_set = test_feature_sets
print len(test_set)

# learn with Naive Bayesian Classifier
classifier = nltk.NaiveBayesClassifier.train(train_set)
accuracy = nltk.classify.accuracy(classifier, test_set)
print "Classification accuracy: " + str(accuracy)

# Show what is the most informative feature?
classifier.show_most_informative_features(10)


