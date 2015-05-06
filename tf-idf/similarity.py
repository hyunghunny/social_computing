# coding=UTF-8

# Similarity Functions
# @author webofthink@snu.ac.kr
#

import math
from reuter import loadReuterDataSet
from reuter import getTDMatrix

##
# Cosine Similarity Function
def cosine_similarity(v1,v2):
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]
        y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)

##
# Document Similarity Model
def compute_similarity(_terms1, _terms2):
    # Take care not to mutate the original data structures
    # since we're in a loop and need the originals multiple times
    terms1 = _terms1.copy()
    terms2 = _terms2.copy()

    # Fill in "gaps" in each map so vectors of the same length can be computed
    for term1 in terms1:
        if term1 not in terms2:
            terms2[term1] = 0
    for term2 in terms2:
        if term2 not in terms1:
            terms1[term2] = 0

    # Create vectors from term maps
    v1 = [score for (term, score) in sorted(terms1.items())]
    v2 = [score for (term, score) in sorted(terms2.items())]

    # Compute similarity amongst documents
    return cosine_similarity(v1, v2)


# Find the most similar document for each one
def findMostSimilarDoc(td_matrix) :
    docs = []
    distances ={}
    for title1 in td_matrix.keys():
        distances[title1] = {}
        max_dist = 0.0
        most_similar = None
        for title2 in td_matrix.keys():
            if title1 == title2:
                continue

            # Compute similarity amongst documents
            terms1 = td_matrix[title1]
            terms2 = td_matrix[title2]
            distances[title1][title2] = compute_similarity(terms1, terms2)

            # nearest if cosine similarity is closed to 1
            if distances[title1][title2] > max_dist:
                max_dist = distances[title1][title2]
                most_similar = title2


        docs.append({
           "doc1" : title1,
           "doc2" : most_similar,
           "distance" : max_dist
        })
    return docs

# Find the most different document for each one
def findMostDifferentDoc(td_matrix) :
    docs = []
    distances ={}
    for title1 in td_matrix.keys():
        distances[title1] = {}

        min_dist = 1.0
        most_different = None
        for title2 in td_matrix.keys():
            if title1 == title2:
                continue

            # Compute similarity amongst documents
            terms1 = td_matrix[title1]
            terms2 = td_matrix[title2]
            distances[title1][title2] = compute_similarity(terms1, terms2)
            # farthest if cosine similarity is closed to 0
            if distances[title1][title2] < min_dist:
                min_dist = distances[title1][title2]
                most_different = title2

        #print title1 + " is most nearest with " + most_similar
        docs.append({
           "doc1" : title1,
           "doc2" : most_different,
           "distance" : min_dist
        })
    return docs


def findFileName(dataset, author) :
    for data in dataset:
        if data['author'] is author :
            return data['filename']

# Reuter data set중 C50test 디렉토리에 있는 50명의 저자의 첫번째 글을 이용하여 다음을 구하세요.
# 가장 cosine similarity가 가까운 작가 pair와 가장 먼 작가 pair를 구하세요

# Read the first article for each author
dataset = loadReuterDataSet("test", True)
print len(dataset)
td_matrix = getTDMatrix(dataset)

most_similar = findMostSimilarDoc(td_matrix)
# Show most nearest cosine similarity
print "Author pairs with most nearest cosine similarity are as below: "
print "****************************************************************"
for doc in sorted(most_similar, key=lambda p: p['distance'], reverse=True) :
    print doc['doc1'] + "'s " + findFileName(dataset, doc['doc1']) + \
          " and " + doc["doc2"] + "'s " + findFileName(dataset, doc['doc2']) + \
          " are the most nearest docs (" + str(doc["distance"]) +")"


most_different = findMostDifferentDoc(td_matrix)
# Show most nearest cosine similarity
print "****************************************************************"
print "Author pairs with most farthest cosine similarity are as below:"
print "****************************************************************"
for doc in sorted(most_different, key=lambda p: p['distance'], reverse=False) :
    print doc['doc1'] + "'s " + findFileName(dataset, doc['doc1']) + \
          " and " + doc["doc2"] + "'s " + findFileName(dataset, doc['doc2']) + \
          " are the most farthest docs (" + str(doc["distance"]) +")"
