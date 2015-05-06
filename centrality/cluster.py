# coding=UTF-8

##
# Cluster algorithms
# @author webofthink@snu.ac.kr
#

from distance import pearson
from distance import euclidean
from distance import tanimoto
from distance import hamdist
from distance import kl
from distance import manhattan

import random

##
# cluster node data structure
#
class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.vec = vec
        self.left = left
        self.right = right
        self.distance = distance
        self.id = id


##
# Hierarchical Clustering algorithm
#
def hcluster(rows, distance=pearson):
    distances = {}
    currentclustid = -1

    # Clusters are initially just the rows
    clust = [bicluster(rows[i], id=i) for i in range(len(rows))]

    while len(clust) > 1:
        lowestpair = (0, 1)

        closest = distance(clust[0].vec, clust[1].vec)

        # loop through every pair looking for the smallest distance
        for i in range(len(clust)):
            for j in range(i + 1, len(clust)):
                # distances is the cache of distance calculations
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)
                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:
                    closest = d
                    lowestpair = (i, j)

        # FIXME: this algorithm makes the prior merged vectors are weaken
        # calculate the average of the two clusters
        mergevec = [(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) /
                    2.0 for i in range(len(clust[0].vec))]

        # create the new cluster
        newcluster = bicluster(mergevec, left=clust[lowestpair[0]], right=clust[lowestpair[1]],
                            distance=closest, id=currentclustid)

        # cluster ids that weren't in the original set are negative
        currentclustid -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]

##
# pretty print cluster data structure(s)
#
def printclust(clust, labels=None, n=0):

    # indent to make a hierarchy layout
    for i in range(n):
        print '',
    if clust.id < 0:
        # negative id means that this is branch
        print '-'
    else:
        # positive id means that this is an endpoint
        if labels == None:
            print clust.id
        else:
            print labels[clust.id]

    # now print the right and left branches
    if clust.left != None:
        printclust(clust.left, labels=labels, n=n + 1)
    if clust.right != None:
        printclust(clust.right, labels=labels, n=n + 1)

##
# save cluster data structure as JSON file
#
def jsonclust(clust, file, last=True, labels=None):

    if clust.id < 0:
        # negative id means that this is branch
        file.write('{ "children": [')
    else:
        # positive id means that this is an endpoint
        if labels == None:
            file.write('{"name": "%s"}' % clust.id)
        else:
            file.write('{"name": "%s"}' % labels[clust.id].replace('"', '').strip())
        if not last:
            file.write(',')

    # now print the right and left branches
    if clust.left != None:
        jsonclust(clust.left, file, False, labels=labels)

    if clust.right != None:
        jsonclust(clust.right, file, True, labels=labels)

    if clust.id < 0:
        if last:
            file.write(']}')
        else:
            file.write(']},')

##
# k-Means clustering algorithm
#
def kcluster(rows, distance=pearson, k=4):

    # Determine the minimum and maximum values for each point
    ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows]))
        for i in range(len(rows[0]))]

    # Create k randomly placed centroids
    clusters = [[random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0]
        for i in range(len(rows[0]))] for j  in range(k)]
    lastmatches = None
    for t in range(100):
        #print 'Iteration %d' % t
        bestmatches = [[] for i in range(k)]

        # Find which centroid is the closest for each row
        for j in range(len(rows)):
            row = rows[j]
            bestmatch = 0
            for i in range(k):
                d = distance(clusters[i], row)
                if d < distance(clusters[bestmatch], row):
                    bestmatch = i
            bestmatches[bestmatch].append(j)

        # If the results are the same as last time, this is complete
        if bestmatches == lastmatches:
            break
        lastmatches = bestmatches

        # Move the centroids to the average of their members
        for i in range(k):
            avgs = [0.0] * len(rows[0])
            if len(bestmatches[i]) > 0:
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m] += rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j] /= len(bestmatches[i])
                clusters[i] = avgs

    return bestmatches