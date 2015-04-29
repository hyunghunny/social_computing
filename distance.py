# coding=UTF-8
##
# Distance algorithms
# @author webofthink@snu.ac.kr
#
from math import sqrt
import numpy as np

# euclidean distance
def euclidean(v1, v2):
    sumSq = 0.0
    for i in range(len(v1)):
        diff = v1[i] - v2[i]
        sumSq += diff * diff
    distance = sqrt(sumSq)
    return distance


# tanimoto distance
def tanimoto(v1, v2):
    c1 = 0
    c2 = 0
    shared = 0
    for i in range(len(v1)):
        if v1[i] != 0: # in v1
            c1 += 1
        if v2[i] != 0: # in v2
            c2 += 1
        if v1[i] != 0 and v2[i] != 0: # in both
            shared += 1
    return 1.0 - float(shared) / (c1 + c2 - shared)

# pearson distance
def pearson(v1, v2):

    # Simple sums
    sum1 = sum(v1)
    sum2 = sum(v2)

    # Sums of the squares
    sum1Sq = sum([v*v for v in v1])
    sum2Sq = sum([v*v for v in v2])

    # Sum of the products
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    # Dimension
    n = float(len(v1))

    # Calculate r (Pearson score)
    eXY = pSum / n

    eX = sum1 / n
    eY = sum2 / n

    eXSq = sum1Sq / n
    eYSq = sum2Sq / n

    numerator = eXY - eX * eY
    denominator = sqrt(eXSq - eX * eX) * sqrt(eYSq - eY * eY)

    if denominator == 0:
        return 0

    return 1.0 - numerator / denominator


# Haming distance - Count the # of differences between equal length strings str1 and str2"""
def hamdist(str1, str2):
    diffs = 0
    for ch1, ch2 in zip(str1, str2):
            if ch1 != ch2:
                    diffs += 1
    return diffs


# Kullback-Leibler distance
def kl(p, q):
    p = np.asarray(p, dtype=np.float)
    q = np.asarray(q, dtype=np.float)
    return np.sum(np.where(p != 0,(p-q) * np.log10(p / q), 0))

# Manhattan distance
def manhattan(xList,yList):
    return float(xList[0]-xList[1]) + abs(yList[0]-yList[1])