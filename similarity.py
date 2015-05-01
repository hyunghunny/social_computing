# coding=UTF-8

# Similarity Functions
# @author webofthink@snu.ac.kr
#

import math

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


# TODO:Reuter data set중 C50test 디렉토리에 있는 50명의 저자의 첫번째 글을 이용하여 다음을 구하세요.
# TODO:가장 cosine similarity가 가까운 작가 pair와 가장 먼 작가 pair를 구하세요
