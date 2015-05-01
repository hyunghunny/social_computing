# coding=UTF-8

##
# Reuter Data Set analysis
#

import os

import nltk

from similarity import compute_similarity


TRAIN_DATA_DIR = '.\\C50\\C50train'

##
# Load Data Set
# if loadOne is True, Read the first article for each author
#
def loadDataSet (loadOne=False) :
    reuter = []
    for authorname in os.listdir(TRAIN_DATA_DIR):
        if authorname.startswith('.'):
            continue
        author_dir = os.path.join(TRAIN_DATA_DIR, authorname)

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
        if loadOne is True:
            break

    return reuter


# Inspecting Data Set
def inspectDataSet (reuter):
    all_content = " ".join([doc['text'] for doc in reuter])

    tokens = all_content.split()
    text = nltk.Text(tokens)

    # Frequency analysis for words of interest
    fdist = text.vocab()
    fdist["U.S."]

    # Frequent collocations in the text (usually meaningful phrases)
    text.collocations()

    QUERY_TERMS = ['china']
    activities = [article['text'].lower().split() for article in reuter]
    # TextCollection provides tf, idf, and tf_idf abstractions so
    # that we don't have to maintain/compute them ourselves
    tc = nltk.TextCollection(activities)

    relevant_activities = []
    for idx in range(len(activities)):
        score = 0
        for term in [t.lower() for t in QUERY_TERMS]:
            score += tc.tf_idf(term, activities[idx])
        if score > 0:
            relevant_activities.append({
                'score': score,
                'author': reuter[idx]['author'],
                'filepath': reuter[idx]['filepath']
            })

    # Sort by score and display results
    relevant_activities = sorted(relevant_activities, key=lambda p: p['score'], reverse=True)

    for activity in relevant_activities[:10]:
        print activity['author']
        print '\tFile: %s' % (activity['filepath'], )
        print '\tScore: %s' % (activity['score'], )
        print


# Compute a term-document matrix such that td_matrix[doc_title][term]
# returns a tf-idf score for the term in the document
def getTDMatrix(reuter) :
    # Preparing td-idf score for each term
    all_articles = [article['text'].lower().split() for article in reuter]
    tc = nltk.TextCollection(all_articles)

    td_matrix = {}
    for idx in range(len(all_articles)):
        article = all_articles[idx]
        fdist = nltk.FreqDist(article)
        doc_title = reuter[idx]['author']
        td_matrix[doc_title] = {}
        for term in fdist.iterkeys():
            td_matrix[doc_title][term] = tc.tf_idf(term, article)
    return td_matrix


# Find the most similar document for each one
def findMostSimilarDoc(td_matrix, distances) :
    for title1 in td_matrix.keys():
        distances[title1] = {}
        min_dist = 1.0
        most_similar = None
        for title2 in td_matrix.keys():
            if title1 == title2:
                continue

            # Compute similarity amongst documents
            terms1 = td_matrix[title1]
            terms2 = td_matrix[title2]
            distances[title1][title2] = compute_similarity(terms1, terms2)
            if distances[title1][title2] < min_dist:
                min_dist = distances[title1][title2]
                most_similar = title2

    return most_similar



# inspects All data set
inspectDataSet(loadDataSet())

# Read the first article for each author
# idx[title1] 와 idx[most_similar] 가 가장 가깝다.
td_matrix = getTDMatrix(loadDataSet(True))

# TODO how to get distances?
distances = False
most_similar = findMostSimilarDoc(td_matrix, distances)