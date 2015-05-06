# coding=UTF-8

##
# Reuter Data Set analysis
#

import os

import nltk

#from similarity import compute_similarity


TRAIN_DATA_DIR = '.\\C50\\C50train'
TEST_DATA_DIR = '.\\C50\\C50test'

##
# Load Data Set
# Set type as "train" to select train data set otherwise test data set will be selected.
#
# if loadOne is True, Read the first article for each author
#
def loadReuterDataSet(type, onlyOne=False) :
    if (type is "train") :
        path = TRAIN_DATA_DIR
        print 'loading data from training data set...'
    else:
        print 'loading data from test data set...'
        path = TEST_DATA_DIR

    reuter = []
    for authorname in os.listdir(path):
        if authorname.startswith('.'):
            continue
        author_dir = os.path.join(path, authorname)
        for filename in os.listdir(author_dir):
            if not filename.endswith('.txt'):
                continue

            filepath = os.path.join(author_dir, filename)
            file = open(filepath, 'r')

            text = file.read()
            reuter += [{'author':authorname,
                'filepath':filepath,
                'filename':filename,
                'text':text}]
            if onlyOne is True:
                break

    return reuter


# Inspecting Data Set
def inspectDataSet(dataset):
    all_content = " ".join([doc['text'] for doc in dataset])

    tokens = all_content.split()
    text = nltk.Text(tokens)

    # Frequency analysis for words of interest
    fdist = text.vocab()
    fdist["U.S."] # XXX:what does it mean?

    # Frequent collocations in the text (usually meaningful phrases)
    text.collocations()


# Compute a term-document matrix such that td_matrix[doc_title][term]
# returns a tf-idf score for the term in the document
def getTDMatrix(reuterData) :
    # Preparing td-idf score for each term
    all_articles = [article['text'].lower().split() for article in reuterData]
    tc = nltk.TextCollection(all_articles)

    td_matrix = {}
    for idx in range(len(all_articles)):
        article = all_articles[idx]
        fdist = nltk.FreqDist(article)
        doc_title = reuterData[idx]['author']
        td_matrix[doc_title] = {}
        for term in fdist.iterkeys():
            td_matrix[doc_title][term] = tc.tf_idf(term, article)
    return td_matrix




QUERY_TERMS = ['china']

