# coding=UTF-8
from math import sqrt

def euclidean(v1, v2):
    sumSq = 0.0
    for i in range(len(v1)):
        diff = v1[i] - v2[i]
        sumSq += diff * diff
    distance = sqrt(sumSq)
    return distance

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


# TODO:Hamming Distance

# TODO:Kullback-Leibler distance

# TODO:Manhattan distance